package main

// HTTP API 响应类型

// ErrorResponse 错误响应
type ErrorResponse struct {
	Error   string `json:"error"`
	Code    string `json:"code"`
	Details any    `json:"details,omitempty"`
}

// SuccessResponse 成功响应
type SuccessResponse struct {
	Success bool   `json:"success"`
	Data    any    `json:"data"`
	Message string `json:"message,omitempty"`
}

// MCP 相关类型（用于内部转换）

// MCPToolResult MCP 工具结果（内部使用）
type MCPToolResult struct {
	Content []MCPContent `json:"content"`
	IsError bool         `json:"isError,omitempty"`
}

// MCPContent MCP 内容（内部使用）
type MCPContent struct {
	Type     string `json:"type"`
	Text     string `json:"text"`
	MimeType string `json:"mimeType"`
	Data     string `json:"data"`
}

// CommentLoadConfig 评论加载配置
type CommentLoadConfig struct {
	ClickMoreReplies   bool   `json:"click_more_replies,omitempty"`
	MaxRepliesThreshold int   `json:"max_replies_threshold,omitempty"`
	MaxCommentItems    int    `json:"max_comment_items,omitempty"`
	ScrollSpeed        string `json:"scroll_speed,omitempty"`
}

// FeedDetailRequest Feed详情请求
type FeedDetailRequest struct {
	FeedID          string             `json:"feed_id" binding:"required"`
	XsecToken       string             `json:"xsec_token" binding:"required"`
	LoadAllComments bool               `json:"load_all_comments,omitempty"`
	CommentConfig   *CommentLoadConfig `json:"comment_config,omitempty"`
}

type SearchFeedsRequest struct {
	Keyword string `json:"keyword" binding:"required"`
	Filters any    `json:"filters,omitempty"`
}

type FeedDetailResponse struct {
	FeedID string `json:"feed_id"`
	Data   any    `json:"data"`
}

type PostCommentRequest struct {
	FeedID    string `json:"feed_id" binding:"required"`
	XsecToken string `json:"xsec_token" binding:"required"`
	Content   string `json:"content" binding:"required"`
}

type PostCommentResponse struct {
	FeedID  string `json:"feed_id"`
	Success bool   `json:"success"`
	Message string `json:"message"`
}

type ReplyCommentRequest struct {
	FeedID    string `json:"feed_id" binding:"required"`
	XsecToken string `json:"xsec_token" binding:"required"`
	CommentID string `json:"comment_id" binding:"required_without=UserID"`
	UserID    string `json:"user_id" binding:"required_without=CommentID"`
	Content   string `json:"content" binding:"required"`
}

type ReplyCommentResponse struct {
	FeedID          string `json:"feed_id"`
	TargetCommentID string `json:"target_comment_id,omitempty"`
	TargetUserID    string `json:"target_user_id,omitempty"`
	Success         bool   `json:"success"`
	Message         string `json:"message"`
}

type UserProfileRequest struct {
	UserID    string `json:"user_id" binding:"required"`
	XsecToken string `json:"xsec_token" binding:"required"`
}

type ActionResult struct {
	FeedID  string `json:"feed_id"`
	Success bool   `json:"success"`
	Message string `json:"message"`
}

type Feed struct {
	Title     string `json:"title"`
	FeedID    string `json:"feed_id"`
	XsecToken string `json:"xsec_token"`
}

type FeedsListResponse struct {
	Feeds []Feed `json:"feeds"`
	Count int    `json:"count"`
}

type UserBasicInfo struct {
	Nickname string `json:"nickname"`
	UserID   string `json:"user_id"`
}

type UserProfileResponse struct {
	UserBasicInfo UserBasicInfo `json:"userBasicInfo"`
	Interactions  []any         `json:"interactions"`
	Feeds         []Feed        `json:"feeds"`
}
