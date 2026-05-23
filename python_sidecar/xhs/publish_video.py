import asyncio
import logging
from python_sidecar.agent_browser import (
    run, open_page, snapshot, click, fill, upload,
)
from python_sidecar.xhs.types import PublishVideoRequest

logger = logging.getLogger(__name__)

PUBLISH_URL = "https://creator.xiaohongshu.com/publish/publish?source=official"


async def publish_video(req: PublishVideoRequest) -> dict:
    await open_page(PUBLISH_URL)
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "上传视频" in line:
            ref = line.split("[ref=")[-1].rstrip("]")
            await click(ref)
            break
    await asyncio.sleep(2)

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "upload" in line.lower() or "上传" in line:
            ref = line.split("[ref=")[-1].rstrip("]")
            await upload(ref, req.video)
            break
    await asyncio.sleep(5)

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "标题" in line and "textbox" in line.lower():
            ref = line.split("[ref=")[-1].rstrip("]")
            await fill(ref, req.title)
            break

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "正文" in line and "textbox" in line.lower():
            ref = line.split("[ref=")[-1].rstrip("]")
            await fill(ref, req.content)
            break

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "发布" in line and "button" in line.lower():
            ref = line.split("[ref=")[-1].rstrip("]")
            await click(ref)
            break
    await asyncio.sleep(3)

    return {"status": "发布完成", "post_id": ""}
