import sys
import os
from unittest.mock import AsyncMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest


@pytest.fixture
def mock_agent_browser():
    """Mock all agent-browser async functions to return controlled snapshots."""
    with patch("python_sidecar.agent_browser.run", new_callable=AsyncMock) as mock_run, \
         patch("python_sidecar.agent_browser.open_page", new_callable=AsyncMock) as mock_open, \
         patch("python_sidecar.agent_browser.snapshot", new_callable=AsyncMock) as mock_snap, \
         patch("python_sidecar.agent_browser.click", new_callable=AsyncMock) as mock_click, \
         patch("python_sidecar.agent_browser.fill", new_callable=AsyncMock) as mock_fill, \
         patch("python_sidecar.agent_browser.upload", new_callable=AsyncMock) as mock_upload, \
         patch("python_sidecar.agent_browser.screenshot", new_callable=AsyncMock) as mock_ss, \
         patch("python_sidecar.agent_browser.scroll", new_callable=AsyncMock) as mock_scroll:
        yield {
            "run": mock_run,
            "open_page": mock_open,
            "snapshot": mock_snap,
            "click": mock_click,
            "fill": mock_fill,
            "upload": mock_upload,
            "screenshot": mock_ss,
            "scroll": mock_scroll,
        }


SAMPLE_PUBLISH_SNAPSHOT = """\
button "上传图文" [ref=e1]
button "上传视频" [ref=e2]
textbox "标题" [ref=e3]
textbox "正文" [ref=e4]
button "添加话题" [ref=e5]
button "发布" [ref=e6]
textbox "" [ref=e7]
button "发送" [ref=e8]
"""

SAMPLE_LOGGED_IN_SNAPSHOT = """\
link "发布图文" [ref=e1]
link "创作中心" [ref=e2]
"""

SAMPLE_LOGGED_OUT_SNAPSHOT = """\
link "登录" [ref=e1]
button "扫码登录" [ref=e2]
"""
