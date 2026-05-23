package main

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

func (s *AppServer) errorHandlingMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Next()

		if len(c.Errors) > 0 {
			c.JSON(http.StatusInternalServerError, ErrorResponse{
				Error: c.Errors.Last().Error(),
				Code:  "internal_error",
			})
		}
	}
}

func (s *AppServer) healthHandler(c *gin.Context) {
	c.JSON(http.StatusOK, SuccessResponse{Success: true, Message: "healthy"})
}

func (s *AppServer) checkLoginStatusHandler(c *gin.Context) {
	status, err := s.xiaohongshuService.CheckLoginStatus(c.Request.Context())
	if err != nil {
		logrus.Errorf("检查登录状态失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, SuccessResponse{Data: status})
}

func (s *AppServer) getLoginQrcodeHandler(c *gin.Context) {
	result, err := s.xiaohongshuService.GetLoginQrcode(c.Request.Context())
	if err != nil {
		logrus.Errorf("获取登录二维码失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, SuccessResponse{Data: result})
}

func (s *AppServer) deleteCookiesHandler(c *gin.Context) {
	err := s.xiaohongshuService.DeleteCookies(c.Request.Context())
	if err != nil {
		logrus.Errorf("删除cookies失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}
	c.JSON(http.StatusOK, SuccessResponse{Success: true, Message: "cookies 已删除"})
}

func (s *AppServer) publishHandler(c *gin.Context) {
	var req PublishRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		logrus.Errorf("绑定发布请求失败: %v", err)
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
		return
	}

	result, err := s.xiaohongshuService.PublishContent(c.Request.Context(), &req)
	if err != nil {
		logrus.Errorf("发布内容失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}
	c.JSON(http.StatusOK, SuccessResponse{Data: result})
}

func (s *AppServer) publishVideoHandler(c *gin.Context) {
	var req PublishVideoRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		logrus.Errorf("绑定视频发布请求失败: %v", err)
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
		return
	}

	result, err := s.xiaohongshuService.PublishVideo(c.Request.Context(), &req)
	if err != nil {
		logrus.Errorf("发布视频失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, SuccessResponse{Data: result})
}

func (s *AppServer) listFeedsHandler(c *gin.Context) {
	result, err := s.xiaohongshuService.ListFeeds(c.Request.Context())
	if err != nil {
		logrus.Errorf("获取Feeds列表失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, SuccessResponse{Data: result})
}

func (s *AppServer) searchFeedsHandler(c *gin.Context) {
	keyword := c.Query("keyword")
	if keyword == "" {
		var req SearchFeedsRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
			return
		}
		keyword = req.Keyword
	}

	if keyword == "" {
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: "keyword is required"})
		return
	}

	result, err := s.xiaohongshuService.SearchFeeds(c.Request.Context(), keyword)
	if err != nil {
		logrus.Errorf("搜索Feeds失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, SuccessResponse{Data: result})
}

func (s *AppServer) getFeedDetailHandler(c *gin.Context) {
	var req FeedDetailRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		logrus.Errorf("绑定Feed详情请求失败: %v", err)
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
		return
	}

	result, err := s.xiaohongshuService.GetFeedDetail(c.Request.Context(), req.FeedID, req.XsecToken, req.LoadAllComments)
	if err != nil {
		logrus.Errorf("获取Feed详情失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, SuccessResponse{Data: result})
}

func (s *AppServer) userProfileHandler(c *gin.Context) {
	var req UserProfileRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		logrus.Errorf("绑定用户主页请求失败: %v", err)
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
		return
	}

	result, err := s.xiaohongshuService.UserProfile(c.Request.Context(), req.UserID, req.XsecToken)
	if err != nil {
		logrus.Errorf("获取用户信息失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, SuccessResponse{Data: result})
}

func (s *AppServer) postCommentHandler(c *gin.Context) {
	var req PostCommentRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		logrus.Errorf("绑定评论请求失败: %v", err)
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
		return
	}

	result, err := s.xiaohongshuService.PostCommentToFeed(c.Request.Context(), req.FeedID, req.XsecToken, req.Content)
	if err != nil {
		logrus.Errorf("发表评论失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, SuccessResponse{Data: result})
}

func (s *AppServer) replyCommentHandler(c *gin.Context) {
	var req ReplyCommentRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		logrus.Errorf("绑定回复评论请求失败: %v", err)
		c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
		return
	}

	result, err := s.xiaohongshuService.ReplyCommentToFeed(c.Request.Context(), req.FeedID, req.XsecToken, req.CommentID, req.UserID, req.Content)
	if err != nil {
		logrus.Errorf("回复评论失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, SuccessResponse{Data: result})
}

func (s *AppServer) healthCheck(c *gin.Context) {
	serviceName := "xiaohongshu-mcp"
	port := c.Request.Host

	c.JSON(http.StatusOK, gin.H{
		"service":   "xiaohongshu-mcp",
		"status":    "running",
		"port":      port,
		"service":   serviceName,
	})
}

func (s *AppServer) myProfileHandler(c *gin.Context) {
	result, err := s.xiaohongshuService.GetMyProfile(c.Request.Context())
	if err != nil {
		logrus.Errorf("获取个人主页失败: %v", err)
		c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
		return
	}

	c.JSON(http.StatusOK, SuccessResponse{Data: result})
}

func (s *AppServer) checkLoginStatus(ctx *gin.Context) {
	status, err := s.xiaohongshuService.CheckLoginStatus(ctx.Request.Context())
	if err != nil {
		ctx.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	ctx.JSON(http.StatusOK, gin.H{
		"is_logged_in": status.IsLoggedIn,
		"username":     status.Username,
	})
}

func (s *AppServer) checkLoginStatusAPI(c *gin.Context) {
	status, err := s.xiaohongshuService.CheckLoginStatus(c.Request.Context())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"ok":    false,
			"error": err.Error(),
		})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"ok": true,
		"data": gin.H{
			"is_logged_in": status.IsLoggedIn,
			"username":     status.Username,
		},
	})
}

func parseIntParam(ctx *gin.Context, key string, defaultVal int) int {
	val := ctx.Query(key)
	if val == "" {
		return defaultVal
	}
	if i, err := strconv.Atoi(val); err == nil {
		return i
	}
	return defaultVal
}
