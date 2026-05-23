package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"

	"github.com/avast/retry-go/v4"
	"github.com/pkg/errors"
	"github.com/sirupsen/logrus"
	"github.com/xpzouying/xiaohongshu-mcp/configs"
	"github.com/xpzouying/xiaohongshu-mcp/pkg/downloader"
	"github.com/xpzouying/xiaohongshu-mcp/pkg/xhsutil"
)

type XiaohongshuService struct {
	httpClient *http.Client
}

func NewXiaohongshuService() *XiaohongshuService {
	return &XiaohongshuService{
		httpClient: &http.Client{Timeout: 30 * time.Second},
	}
}

type PublishRequest struct {
	Title      string   `json:"title"`
	Content    string   `json:"content"`
	Images     []string `json:"images"`
	Tags       []string `json:"tags,omitempty"`
	ScheduleAt string   `json:"schedule_at,omitempty"`
	IsOriginal bool     `json:"is_original,omitempty"`
	Visibility string   `json:"visibility,omitempty"`
	Products   []string `json:"products,omitempty"`
}

type PublishVideoRequest struct {
	Title      string   `json:"title"`
	Content    string   `json:"content"`
	Video      string   `json:"video"`
	Tags       []string `json:"tags,omitempty"`
	ScheduleAt string   `json:"schedule_at,omitempty"`
	Visibility string   `json:"visibility,omitempty"`
	Products   []string `json:"products,omitempty"`
}

type PublishResponse struct {
	Title   string `json:"title"`
	Content string `json:"content"`
	Images  int    `json:"images"`
	Status  string `json:"status"`
	PostID  string `json:"post_id,omitempty"`
}

type PublishVideoResponse struct {
	Title   string `json:"title"`
	Content string `json:"content"`
	Video   string `json:"video"`
	Status  string `json:"status"`
	PostID  string `json:"post_id,omitempty"`
}

type LoginStatusResponse struct {
	IsLoggedIn bool   `json:"is_logged_in"`
	Username   string `json:"username,omitempty"`
}

type LoginQrcodeResponse struct {
	Timeout    string `json:"timeout"`
	IsLoggedIn bool   `json:"is_logged_in"`
	Img        string `json:"img,omitempty"`
}

type sidecarResponse struct {
	Ok      bool            `json:"ok"`
	Data    json.RawMessage `json:"data"`
	Error   string          `json:"error"`
	Message string          `json:"message"`
}

func (s *XiaohongshuService) callSidecar(ctx context.Context, method, path string, body any) (*sidecarResponse, error) {
	var reqBody io.Reader
	if body != nil {
		data, err := json.Marshal(body)
		if err != nil {
			return nil, errors.Wrap(err, "marshal request")
		}
		reqBody = bytes.NewReader(data)
	}

	url := configs.GetSidecarURL() + path
	req, err := http.NewRequestWithContext(ctx, method, url, reqBody)
	if err != nil {
		return nil, errors.Wrap(err, "create request")
	}
	req.Header.Set("Content-Type", "application/json")

	var resp *http.Response
	err = retry.Do(
		func() error {
			var err error
			resp, err = s.httpClient.Do(req)
			return err
		},
		retry.Attempts(2),
		retry.Delay(100*time.Millisecond),
	)
	if err != nil {
		return nil, errors.Wrap(err, "sidecar unreachable")
	}
	defer resp.Body.Close()

	var result sidecarResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, errors.Wrap(err, "decode sidecar response")
	}
	if !result.Ok {
		return nil, fmt.Errorf("sidecar error [%s]: %s", result.Error, result.Message)
	}
	return &result, nil
}

func (s *XiaohongshuService) callSidecarOK(ctx context.Context, method, path string, body any) error {
	_, err := s.callSidecar(ctx, method, path, body)
	return err
}

func (s *XiaohongshuService) CheckLoginStatus(ctx context.Context) (*LoginStatusResponse, error) {
	resp, err := s.callSidecar(ctx, http.MethodPost, "/login/status", nil)
	if err != nil {
		return nil, err
	}
	var data LoginStatusResponse
	json.Unmarshal(resp.Data, &data)
	return &data, nil
}

func (s *XiaohongshuService) GetLoginQrcode(ctx context.Context) (*LoginQrcodeResponse, error) {
	resp, err := s.callSidecar(ctx, http.MethodPost, "/login/qrcode", nil)
	if err != nil {
		return nil, err
	}
	var data LoginQrcodeResponse
	json.Unmarshal(resp.Data, &data)
	return &data, nil
}

func (s *XiaohongshuService) DeleteCookies(ctx context.Context) error {
	return s.callSidecarOK(ctx, http.MethodDelete, "/login/cookies", nil)
}

func (s *XiaohongshuService) PublishContent(ctx context.Context, req *PublishRequest) (*PublishResponse, error) {
	if xhsutil.CalcTitleLength(req.Title) > 20 {
		return nil, fmt.Errorf("标题长度超过限制")
	}
	imagePaths, err := downloader.NewImageProcessor().ProcessImages(req.Images)
	if err != nil {
		return nil, err
	}
	req.Images = imagePaths
	_, err = s.callSidecar(ctx, http.MethodPost, "/publish", req)
	if err != nil {
		return nil, err
	}
	return &PublishResponse{Title: req.Title, Content: req.Content, Images: len(imagePaths), Status: "发布完成"}, nil
}

func (s *XiaohongshuService) PublishVideo(ctx context.Context, req *PublishVideoRequest) (*PublishVideoResponse, error) {
	if xhsutil.CalcTitleLength(req.Title) > 20 {
		return nil, fmt.Errorf("标题长度超过限制")
	}
	_, err := s.callSidecar(ctx, http.MethodPost, "/publish_video", req)
	if err != nil {
		return nil, err
	}
	return &PublishVideoResponse{Title: req.Title, Video: req.Video, Status: "发布完成"}, nil
}

func (s *XiaohongshuService) ListFeeds(ctx context.Context) (*FeedsListResponse, error) {
	resp, err := s.callSidecar(ctx, http.MethodGet, "/feeds/list", nil)
	if err != nil {
		return nil, err
	}
	var result FeedsListResponse
	json.Unmarshal(resp.Data, &result)
	return &result, nil
}

func (s *XiaohongshuService) SearchFeeds(ctx context.Context, keyword string) (*FeedsListResponse, error) {
	resp, err := s.callSidecar(ctx, http.MethodPost, "/feeds/search", map[string]string{"keyword": keyword})
	if err != nil {
		return nil, err
	}
	var result FeedsListResponse
	json.Unmarshal(resp.Data, &result)
	return &result, nil
}

func (s *XiaohongshuService) GetFeedDetail(ctx context.Context, feedID, xsecToken string, loadAllComments bool) (*FeedDetailResponse, error) {
	resp, err := s.callSidecar(ctx, http.MethodPost, "/feeds/detail", map[string]any{
		"feed_id": feedID, "xsec_token": xsecToken, "load_all_comments": loadAllComments,
	})
	if err != nil {
		return nil, err
	}
	var result FeedDetailResponse
	json.Unmarshal(resp.Data, &result)
	return &result, nil
}

func (s *XiaohongshuService) PostCommentToFeed(ctx context.Context, feedID, xsecToken, content string) (*PostCommentResponse, error) {
	err := s.callSidecarOK(ctx, http.MethodPost, "/feeds/comment", map[string]string{
		"feed_id": feedID, "xsec_token": xsecToken, "content": content,
	})
	if err != nil {
		return nil, err
	}
	return &PostCommentResponse{FeedID: feedID, Success: true, Message: "评论发表成功"}, nil
}

func (s *XiaohongshuService) ReplyCommentToFeed(ctx context.Context, feedID, xsecToken, commentID, userID, content string) (*ReplyCommentResponse, error) {
	err := s.callSidecarOK(ctx, http.MethodPost, "/feeds/comment/reply", map[string]string{
		"feed_id": feedID, "xsec_token": xsecToken, "comment_id": commentID, "user_id": userID, "content": content,
	})
	if err != nil {
		return nil, err
	}
	return &ReplyCommentResponse{FeedID: feedID, TargetCommentID: commentID, TargetUserID: userID, Success: true, Message: "评论回复成功"}, nil
}

func (s *XiaohongshuService) LikeFeed(ctx context.Context, feedID, xsecToken string) (*ActionResult, error) {
	err := s.callSidecarOK(ctx, http.MethodPost, "/like", map[string]string{"feed_id": feedID, "xsec_token": xsecToken})
	if err != nil {
		return nil, err
	}
	return &ActionResult{FeedID: feedID, Success: true, Message: "点赞成功"}, nil
}

func (s *XiaohongshuService) UnlikeFeed(ctx context.Context, feedID, xsecToken string) (*ActionResult, error) {
	err := s.callSidecarOK(ctx, http.MethodPost, "/like", map[string]any{"feed_id": feedID, "xsec_token": xsecToken, "unlike": true})
	if err != nil {
		return nil, err
	}
	return &ActionResult{FeedID: feedID, Success: true, Message: "取消点赞成功"}, nil
}

func (s *XiaohongshuService) FavoriteFeed(ctx context.Context, feedID, xsecToken string) (*ActionResult, error) {
	err := s.callSidecarOK(ctx, http.MethodPost, "/favorite", map[string]string{"feed_id": feedID, "xsec_token": xsecToken})
	if err != nil {
		return nil, err
	}
	return &ActionResult{FeedID: feedID, Success: true, Message: "收藏成功"}, nil
}

func (s *XiaohongshuService) UnfavoriteFeed(ctx context.Context, feedID, xsecToken string) (*ActionResult, error) {
	err := s.callSidecarOK(ctx, http.MethodPost, "/favorite", map[string]any{"feed_id": feedID, "xsec_token": xsecToken, "unfavorite": true})
	if err != nil {
		return nil, err
	}
	return &ActionResult{FeedID: feedID, Success: true, Message: "取消收藏成功"}, nil
}

func (s *XiaohongshuService) UserProfile(ctx context.Context, userID, xsecToken string) (*UserProfileResponse, error) {
	resp, err := s.callSidecar(ctx, http.MethodPost, "/user/profile", map[string]string{
		"user_id": userID, "xsec_token": xsecToken,
	})
	if err != nil {
		return nil, err
	}
	var result UserProfileResponse
	json.Unmarshal(resp.Data, &result)
	return &result, nil
}

func (s *XiaohongshuService) GetMyProfile(ctx context.Context) (*UserProfileResponse, error) {
	resp, err := s.callSidecar(ctx, http.MethodPost, "/login/status", nil)
	if err != nil {
		return nil, err
	}
	var status LoginStatusResponse
	json.Unmarshal(resp.Data, &status)
	return &UserProfileResponse{UserBasicInfo: UserBasicInfo{Nickname: status.Username}}, nil
}
