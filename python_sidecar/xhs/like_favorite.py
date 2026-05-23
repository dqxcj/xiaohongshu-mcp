import asyncio
import logging
from python_sidecar.agent_browser import open_page, snapshot, click

logger = logging.getLogger(__name__)

FEED_URL = "https://www.xiaohongshu.com/explore/{feed_id}"


async def _click_button(feed_id: str, label: str) -> bool:
    """Open a feed page and click a button by label. Returns True if button was found and clicked."""
    await open_page(FEED_URL.format(feed_id=feed_id))
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if label in line and "button" in line.lower():
            ref = line.split("[ref=")[-1].rstrip("]")
            await click(ref)
            return True
    return False


async def like_feed(feed_id: str) -> dict:
    found = await _click_button(feed_id, "点赞")
    if not found:
        raise RuntimeError(f"未找到点赞按钮，可能未登录或 feed_id 无效: {feed_id}")
    return {"success": True, "message": "点赞成功"}


async def unlike_feed(feed_id: str) -> dict:
    found = await _click_button(feed_id, "点赞")
    if not found:
        raise RuntimeError(f"未找到点赞按钮: {feed_id}")
    return {"success": True, "message": "取消点赞成功"}


async def favorite_feed(feed_id: str) -> dict:
    found = await _click_button(feed_id, "收藏")
    if not found:
        raise RuntimeError(f"未找到收藏按钮，可能未登录或 feed_id 无效: {feed_id}")
    return {"success": True, "message": "收藏成功"}


async def unfavorite_feed(feed_id: str) -> dict:
    found = await _click_button(feed_id, "收藏")
    if not found:
        raise RuntimeError(f"未找到收藏按钮: {feed_id}")
    return {"success": True, "message": "取消收藏成功"}
