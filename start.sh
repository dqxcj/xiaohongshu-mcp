#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Starting xiaohongshu-mcp ==="

echo "[1/2] Starting Python sidecar..."
cd "$SCRIPT_DIR/python_sidecar"
pip install -r requirements.txt -q 2>/dev/null
python server.py &
SIDECAR_PID=$!
echo "  Sidecar PID: $SIDECAR_PID"

echo "  Waiting for sidecar..."
for i in $(seq 1 30); do
    if curl -s http://127.0.0.1:18061/health >/dev/null 2>&1; then
        echo "  Sidecar ready!"
        break
    fi
    sleep 1
done

echo "[2/2] Starting Go MCP server..."
cd "$SCRIPT_DIR"
go run . --port :18060 --sidecar http://127.0.0.1:18061

kill $SIDECAR_PID 2>/dev/null
echo "=== Stopped ==="
