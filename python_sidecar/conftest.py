import sys
import os
from unittest.mock import AsyncMock, patch

# Make sure python_sidecar is importable from tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest


@pytest.fixture
def mock_agent_browser():
    """Mock agent-browser async functions in both source and consumer modules.

    Publish/login/feeds modules import via ``from python_sidecar.agent_browser
    import snapshot`` which creates a *local* reference in their own namespace.
    Patching only ``python_sidecar.agent_browser.snapshot`` does NOT affect
    those local references, so we patch consumer module namespaces too.
    """
    from python_sidecar.xhs import login as login_mod
    from python_sidecar.xhs import publish as publish_mod
    from python_sidecar.xhs import publish_video as publish_video_mod
    from python_sidecar.xhs import feeds as feeds_mod
    from python_sidecar.xhs import comment as comment_mod
    from python_sidecar.xhs import like_favorite as like_favorite_mod

    consumers = [login_mod, publish_mod, publish_video_mod, feeds_mod, comment_mod, like_favorite_mod]

    source_patchers = []
    mocks = {}
    for name in ["run", "open_page", "snapshot", "click", "fill", "upload",
                  "screenshot", "scroll"]:
        p = patch(f"python_sidecar.agent_browser.{name}", new_callable=AsyncMock)
        mocked = p.start()
        source_patchers.append(p)
        mocks[name] = mocked

    for mod in consumers:
        for name in mocks:
            setattr(mod, name, mocks[name])

    yield mocks

    for p in source_patchers:
        p.stop()


SAMPLE_PUBLISH_SNAPSHOT = """\
button "上传图文" [ref=e1]
button "上传视频" [ref=e2]
textbox "标题" [ref=e3]
textbox "正文" [ref=e4]
button "添加话题" [ref=e5]
button "发布" [ref=e6]
textbox "" [ref=e7]
button "发送" [ref=e8]
button "upload" [ref=e9]
"""

SAMPLE_LOGGED_IN_SNAPSHOT = """\
link "发布图文" [ref=e1]
link "创作中心" [ref=e2]
"""

SAMPLE_LOGGED_OUT_SNAPSHOT = """\
link "登录" [ref=e1]
button "扫码登录" [ref=e2]
"""
