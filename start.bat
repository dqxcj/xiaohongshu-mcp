@echo off
echo === Starting xiaohongshu-mcp ===

echo [1/2] Starting Python sidecar...
cd /d "%~dp0python_sidecar"
pip install -r requirements.txt -q
start "XHS-Sidecar" /min cmd /c "python server.py"

echo   Waiting for sidecar...
:wait
timeout /t 1 >nul
curl -s http://127.0.0.1:18061/health >nul 2>&1
if errorlevel 1 goto wait
echo   Sidecar ready!

echo [2/2] Starting Go MCP server...
cd /d "%~dp0"
go run . --port :18060 --sidecar http://127.0.0.1:18061
echo === Stopped ===
