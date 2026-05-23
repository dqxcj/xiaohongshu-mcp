import asyncio
import logging
from python_sidecar.agent_browser import (
    run, open_page, snapshot, click, fill, upload,
)
from python_sidecar.xhs.types import PublishVideoRequest
from python_sidecar.xhs.publish import _find_ref, _must_find

logger = logging.getLogger(__name__)

PUBLISH_URL = "https://creator.xiaohongshu.com/publish/publish?source=official"


async def publish_video(req: PublishVideoRequest) -> dict:
    await open_page(PUBLISH_URL)
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    ref = _must_find(snap, "选择视频Tab", "上传视频")
    await click(ref)
    await asyncio.sleep(2)

    snap = await snapshot("-i")
    ref = _must_find(snap, "上传视频文件", "upload")
    await upload(ref, req.video)
    await asyncio.sleep(5)

    snap = await snapshot("-i")
    ref = _must_find(snap, "填写标题", "标题", "textbox")
    await fill(ref, req.title)

    snap = await snapshot("-i")
    ref = _must_find(snap, "填写正文", "正文", "textbox")
    await fill(ref, req.content)

    snap = await snapshot("-i")
    ref = _must_find(snap, "点击发布按钮", "发布", "button")
    await click(ref)
    await asyncio.sleep(3)

    return {"status": "发布完成", "post_id": ""}
