import pytest
from python_sidecar.conftest import SAMPLE_PUBLISH_SNAPSHOT
from python_sidecar.xhs.types import PublishRequest
from python_sidecar.xhs.publish import publish_content


@pytest.mark.asyncio
async def test_publish_content_basic_flow(mock_agent_browser):
    mock_agent_browser["snapshot"].return_value = SAMPLE_PUBLISH_SNAPSHOT

    req = PublishRequest(
        title="测试标题",
        content="测试正文内容",
        images=["/tmp/img1.png", "/tmp/img2.png"],
        tags=["美食", "旅行"],
    )
    result = await publish_content(req)

    assert result["status"] == "发布完成"
    mock_agent_browser["click"].assert_any_call("@e6")


@pytest.mark.asyncio
async def test_publish_finds_upload_tab(mock_agent_browser):
    mock_agent_browser["snapshot"].return_value = SAMPLE_PUBLISH_SNAPSHOT

    req = PublishRequest(title="test", content="test", images=["/tmp/img.png"])
    await publish_content(req)

    mock_agent_browser["click"].assert_any_call("@e1")
