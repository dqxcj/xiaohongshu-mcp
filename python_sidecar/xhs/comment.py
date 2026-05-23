import asyncio
import logging
from python_sidecar.agent_browser import open_page, snapshot, fill, click

logger = logging.getLogger(__name__)

FEED_URL = "https://www.xiaohongshu.com/explore/{feed_id}"


async def post_comment(feed_id: str, content: str) -> dict:
    await open_page(FEED_URL.format(feed_id=feed_id))
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "评论" in line and "textbox" in line.lower():
            ref = line.split("[ref=")[-1].rstrip("]")
            await click(ref)
            await fill(ref, content)
            await asyncio.sleep(0.5)
            snap2 = await snapshot("-i")
            for l2 in snap2.split("\n"):
                if "发送" in l2 and "button" in l2.lower():
                    r2 = l2.split("[ref=")[-1].rstrip("]")
                    await click(r2)
                    break
            break

    return {"success": True, "message": "评论发表成功"}


async def reply_comment(feed_id: str, comment_id: str, content: str) -> dict:
    await open_page(FEED_URL.format(feed_id=feed_id))
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "回复" in line and "button" in line.lower():
            ref = line.split("[ref=")[-1].rstrip("]")
            await click(ref)
            await asyncio.sleep(0.5)
            snap2 = await snapshot("-i")
            for l2 in snap2.split("\n"):
                if "textbox" in l2.lower():
                    r2 = l2.split("[ref=")[-1].rstrip("]")
                    await fill(r2, content)
                    break
            break

    return {"success": True, "message": "评论回复成功"}
