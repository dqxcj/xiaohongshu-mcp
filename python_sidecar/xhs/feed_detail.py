import asyncio
import logging
from python_sidecar.agent_browser import open_page, snapshot, scroll

logger = logging.getLogger(__name__)

FEED_URL = "https://www.xiaohongshu.com/explore/{feed_id}"


async def get_feed_detail(feed_id: str, load_all_comments: bool = False) -> dict:
    await open_page(FEED_URL.format(feed_id=feed_id))
    await asyncio.sleep(3)

    snap = await snapshot("-i")

    comments = []
    if load_all_comments:
        for _ in range(5):
            await scroll("down")
            await asyncio.sleep(1)
        snap = await snapshot("-i")

    return {
        "feed_id": feed_id,
        "snapshot": snap,
        "comments": comments,
    }
