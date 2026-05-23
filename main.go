package main

import (
	"flag"

	"github.com/sirupsen/logrus"
	"github.com/xpzouying/xiaohongshu-mcp/configs"
)

func main() {
	var (
		port       string
		sidecarURL string
	)
	flag.StringVar(&port, "port", ":18060", "MCP 服务端口")
	flag.StringVar(&sidecarURL, "sidecar", "http://127.0.0.1:18061", "Python sidecar 地址")
	flag.Parse()

	configs.SetSidecarURL(sidecarURL)

	xiaohongshuService := NewXiaohongshuService()
	appServer := NewAppServer(xiaohongshuService)
	if err := appServer.Start(port); err != nil {
		logrus.Fatalf("failed to run server: %v", err)
	}
}
