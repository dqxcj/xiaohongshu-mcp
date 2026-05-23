package main

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/sirupsen/logrus"
)

func (s *AppServer) handleCheckLoginStatus(ctx context.Context) *MCPToolResult {
	status, err := s.xiaohongshuService.CheckLoginStatus(ctx)
	if err != nil {
		return &MCPToolResult{
			IsError: true,
			Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("检查登录状态失败: %v", err)}},
		}
	}
	if !status.IsLoggedIn {
		return &MCPToolResult{
			IsError: false,
			Content: []MCPContent{{Type: "text", Text: "❌ 未登录，请先登录小红书账号"}},
		}
	}
	return &MCPToolResult{
		Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("✅ 已登录，用户名: %s", status.Username)}},
	}
}

func (s *AppServer) handleGetLoginQrcode(ctx context.Context) *MCPToolResult {
	result, err := s.xiaohongshuService.GetLoginQrcode(ctx)
	if err != nil {
		return &MCPToolResult{
			IsError: true,
			Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("获取登录二维码失败: %v", err)}},
		}
	}

	if result.IsLoggedIn {
		return &MCPToolResult{
			Content: []MCPContent{{Type: "text", Text: "✅ 已登录，无需扫码"}},
		}
	}

	if result.Img != "" {
		return &MCPToolResult{
			Content: []MCPContent{
				{Type: "text", Text: fmt.Sprintf("📱 请使用小红书 App 扫描二维码登录\n⏰ 超时时间: %s\n请在手机上确认登录", result.Timeout)},
				{Type: "image", Data: result.Img, MimeType: "image/png"},
			},
		}
	}

	return &MCPToolResult{
		Content: []MCPContent{
			{Type: "text", Text: fmt.Sprintf("📱 请查看 /tmp/xhs_qrcode.png 文件\n⏰ 超时时间: %s\n请在手机上确认登录", result.Timeout)},
		},
	}
}

func (s *AppServer) handleDeleteCookies(ctx context.Context) *MCPToolResult {
	err := s.xiaohongshuService.DeleteCookies(ctx)
	if err != nil {
		return &MCPToolResult{
			IsError: true,
			Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("删除cookies失败: %v", err)}},
		}
	}
	return &MCPToolResult{Content: []MCPContent{{Type: "text", Text: "cookies 已删除"}}}
}

func (s *AppServer) handlePublishContent(ctx context.Context, args map[string]interface{}) *MCPToolResult {
	title, _ := args["title"].(string)
	content, _ := args["content"].(string)
	images, _ := args["images"].([]interface{})
	tags, _ := args["tags"].([]interface{})
	scheduleAt, _ := args["schedule_at"].(string)
	isOriginal, _ := args["is_original"].(bool)
	visibility, _ := args["visibility"].(string)
	products, _ := args["products"].([]interface{})

	if title == "" || content == "" || len(images) == 0 {
		return &MCPToolResult{IsError: true, Content: []MCPContent{{Type: "text", Text: "缺少必要参数: title, content, images"}}}
	}

	imageStrs := make([]string, len(images))
	for i, img := range images {
		imageStrs[i], _ = img.(string)
	}

	tagStrs := make([]string, len(tags))
	for i, t := range tags {
		tagStrs[i], _ = t.(string)
	}

	productStrs := make([]string, len(products))
	for i, p := range products {
		productStrs[i], _ = p.(string)
	}

	req := &PublishRequest{
		Title:      title,
		Content:    content,
		Images:     imageStrs,
		Tags:       tagStrs,
		ScheduleAt: scheduleAt,
		IsOriginal: isOriginal,
		Visibility: visibility,
		Products:   productStrs,
	}

	result, err := s.xiaohongshuService.PublishContent(ctx, req)
	if err != nil {
		return &MCPToolResult{
			IsError: true,
			Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("发布失败: %v", err)}},
		}
	}

	data, _ := json.Marshal(result)
	return &MCPToolResult{Content: []MCPContent{{Type: "text", Text: "发布完成: " + string(data)}}}
}

func (s *AppServer) handlePublishVideo(ctx context.Context, args map[string]interface{}) *MCPToolResult {
	title, _ := args["title"].(string)
	content, _ := args["content"].(string)
	video, _ := args["video"].(string)
	tags, _ := args["tags"].([]interface{})
	scheduleAt, _ := args["schedule_at"].(string)
	visibility, _ := args["visibility"].(string)
	products, _ := args["products"].([]interface{})

	if title == "" || content == "" || video == "" {
		return &MCPToolResult{IsError: true, Content: []MCPContent{{Type: "text", Text: "缺少必要参数: title, content, video"}}}
	}

	tagStrs := make([]string, len(tags))
	for i, t := range tags {
		tagStrs[i], _ = t.(string)
	}

	productStrs := make([]string, len(products))
	for i, p := range products {
		productStrs[i], _ = p.(string)
	}

	req := &PublishVideoRequest{
		Title:      title,
		Content:    content,
		Video:      video,
		Tags:       tagStrs,
		ScheduleAt: scheduleAt,
		Visibility: visibility,
		Products:   productStrs,
	}

	result, err := s.xiaohongshuService.PublishVideo(ctx, req)
	if err != nil {
		return &MCPToolResult{
			IsError: true,
			Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("发布视频失败: %v", err)}},
		}
	}

	data, _ := json.Marshal(result)
	return &MCPToolResult{Content: []MCPContent{{Type: "text", Text: "发布完成: " + string(data)}}}
}

func (s *AppServer) handleListFeeds(ctx context.Context) *MCPToolResult {
	result, err := s.xiaohongshuService.ListFeeds(ctx)
	if err != nil {
		return &MCPToolResult{
			IsError: true,
			Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("获取Feeds列表失败: %v", err)}},
		}
	}

	data, _ := json.Marshal(result)
	return &MCPToolResult{Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("共找到 %d 条Feed:", result.Count) + string(data)}}}
}

func (s *AppServer) handleSearchFeeds(ctx context.Context, args SearchFeedsArgs) *MCPToolResult {
	if args.Keyword == "" {
		return &MCPToolResult{IsError: true, Content: []MCPContent{{Type: "text", Text: "缺少搜索关键词"}}}
	}

	result, err := s.xiaohongshuService.SearchFeeds(ctx, args.Keyword)
	if err != nil {
		return &MCPToolResult{
			IsError: true,
			Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("搜索失败: %v", err)}},
		}
	}

	data, _ := json.Marshal(result)
	return &MCPToolResult{Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("搜索完成，找到 %d 条结果:", result.Count) + string(data)}}}
}

func (s *AppServer) handleGetFeedDetail(ctx context.Context, args map[string]interface{}) *MCPToolResult {
	feedID, _ := args["feed_id"].(string)
	xsecToken, _ := args["xsec_token"].(string)
	loadAll, _ := args["load_all_comments"].(bool)

	result, err := s.xiaohongshuService.GetFeedDetail(ctx, feedID, xsecToken, loadAll)
	if err != nil {
		return &MCPToolResult{
			IsError: true,
			Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("获取Feed详情失败: %v", err)}},
		}
	}

	data, _ := json.Marshal(result)
	return &MCPToolResult{Content: []MCPContent{{Type: "text", Text: "Feed详情: " + string(data)}}}
}

func (s *AppServer) handleUserProfile(ctx context.Context, args map[string]interface{}) *MCPToolResult {
	userID, _ := args["user_id"].(string)
	xsecToken, _ := args["xsec_token"].(string)

	if userID == "" || xsecToken == "" {
		return &MCPToolResult{IsError: true, Content: []MCPContent{{Type: "text", Text: "缺少必要参数: user_id, xsec_token"}}}
	}

	result, err := s.xiaohongshuService.UserProfile(ctx, userID, xsecToken)
	if err != nil {
		return &MCPToolResult{
			IsError: true,
			Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("获取用户主页失败: %v", err)}},
		}
	}

	data, _ := json.Marshal(result)
	return &MCPToolResult{Content: []MCPContent{{Type: "text", Text: "用户主页: " + string(data)}}}
}

func (s *AppServer) handlePostComment(ctx context.Context, args map[string]interface{}) *MCPToolResult {
	feedID, _ := args["feed_id"].(string)
	xsecToken, _ := args["xsec_token"].(string)
	content, _ := args["content"].(string)

	if feedID == "" || xsecToken == "" || content == "" {
		return &MCPToolResult{IsError: true, Content: []MCPContent{{Type: "text", Text: "缺少必要参数: feed_id, xsec_token, content"}}}
	}

	result, err := s.xiaohongshuService.PostCommentToFeed(ctx, feedID, xsecToken, content)
	if err != nil {
		return &MCPToolResult{
			IsError: true,
			Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("发表评论失败: %v", err)}},
		}
	}

	data, _ := json.Marshal(result)
	return &MCPToolResult{Content: []MCPContent{{Type: "text", Text: "评论发表: " + string(data)}}}
}

func (s *AppServer) handleReplyComment(ctx context.Context, args map[string]interface{}) *MCPToolResult {
	feedID, _ := args["feed_id"].(string)
	xsecToken, _ := args["xsec_token"].(string)
	commentID, _ := args["comment_id"].(string)
	userID, _ := args["user_id"].(string)
	content, _ := args["content"].(string)

	result, err := s.xiaohongshuService.ReplyCommentToFeed(ctx, feedID, xsecToken, commentID, userID, content)
	if err != nil {
		return &MCPToolResult{
			IsError: true,
			Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("回复评论失败: %v", err)}},
		}
	}

	data, _ := json.Marshal(result)
	return &MCPToolResult{Content: []MCPContent{{Type: "text", Text: "评论回复: " + string(data)}}}
}

func (s *AppServer) handleLikeFeed(ctx context.Context, args map[string]interface{}) *MCPToolResult {
	feedID, _ := args["feed_id"].(string)
	xsecToken, _ := args["xsec_token"].(string)
	unlike, _ := args["unlike"].(bool)

	var res *ActionResult
	var err error
	if unlike {
		res, err = s.xiaohongshuService.UnlikeFeed(ctx, feedID, xsecToken)
	} else {
		res, err = s.xiaohongshuService.LikeFeed(ctx, feedID, xsecToken)
	}
	if err != nil {
		return &MCPToolResult{IsError: true, Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("操作失败: %v", err)}}}
	}
	data, _ := json.Marshal(res)
	return &MCPToolResult{Content: []MCPContent{{Type: "text", Text: string(data)}}}
}

func (s *AppServer) handleFavoriteFeed(ctx context.Context, args map[string]interface{}) *MCPToolResult {
	feedID, _ := args["feed_id"].(string)
	xsecToken, _ := args["xsec_token"].(string)
	unfavorite, _ := args["unfavorite"].(bool)

	var res *ActionResult
	var err error
	if unfavorite {
		res, err = s.xiaohongshuService.UnfavoriteFeed(ctx, feedID, xsecToken)
	} else {
		res, err = s.xiaohongshuService.FavoriteFeed(ctx, feedID, xsecToken)
	}
	if err != nil {
		return &MCPToolResult{IsError: true, Content: []MCPContent{{Type: "text", Text: fmt.Sprintf("操作失败: %v", err)}}}
	}
	data, _ := json.Marshal(res)
	return &MCPToolResult{Content: []MCPContent{{Type: "text", Text: string(data)}}}
}
