import asyncio
import logging
from python_sidecar.agent_browser import open_page, snapshot, click

logger = logging.getLogger(__name__)

FEED_URL = "https://www.xiaohongshu.com/explore/{feed_id}"


async def like_feed(feed_id: str) -> dict:
    await open_page(FEED_URL.format(feed_id=feed_id))
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "点赞" in line and "button" in line.lower():
            ref = line.split("[ref=")[-1].rstrip("]")
            await click(ref)
            break

    return {"success": True, "message": "点赞成功或已点赞"}


async def unlike_feed(feed_id: str) -> dict:
    return await like_feed(feed_id)


async def favorite_feed(feed_id: str) -> dict:
    await open_page(FEED_URL.format(feed_id=feed_id))
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "收藏" in line and "button" in line.lower():
            ref = line.split("[ref=")[-1].rstrip("]")
            await click(ref)
            break

    return {"success": True, "message": "收藏成功或已收藏"}


async def unfavorite_feed(feed_id: str) -> dict:
    return await favorite_feed(feed_id)
