import asyncio
import logging
from python_sidecar.agent_browser import (
    run, open_page, snapshot, click, fill, upload,
)
from python_sidecar.xhs.types import PublishRequest

logger = logging.getLogger(__name__)

PUBLISH_URL = "https://creator.xiaohongshu.com/publish/publish?source=official"


async def publish_content(req: PublishRequest) -> dict:
    await open_page(PUBLISH_URL)
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "上传图文" in line:
            ref = line.split("[ref=")[-1].rstrip("]")
            await click(ref)
            break
    await asyncio.sleep(2)

    for img_path in req.images:
        snap = await snapshot("-i")
        for line in snap.split("\n"):
            if "upload" in line.lower() or "上传" in line:
                ref = line.split("[ref=")[-1].rstrip("]")
                await upload(ref, img_path)
                break
        await asyncio.sleep(1)

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

    for tag in req.tags[:10]:
        snap = await snapshot("-i")
        for line in snap.split("\n"):
            if "添加话题" in line:
                ref = line.split("[ref=")[-1].rstrip("]")
                await click(ref)
                await asyncio.sleep(0.5)
                snap = await snapshot("-i")
                for l2 in snap.split("\n"):
                    if "textbox" in l2.lower():
                        r2 = l2.split("[ref=")[-1].rstrip("]")
                        await fill(r2, tag)
                        await asyncio.sleep(0.5)
                        break
                break

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "发布" in line and "button" in line.lower():
            ref = line.split("[ref=")[-1].rstrip("]")
            await click(ref)
            break

    await asyncio.sleep(3)
    return {"status": "发布完成", "post_id": ""}
