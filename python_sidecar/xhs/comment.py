import asyncio
import logging
from python_sidecar.agent_browser import open_page, snapshot, fill, click
from python_sidecar.xhs.publish import _find_ref, _must_find

logger = logging.getLogger(__name__)

FEED_URL = "https://www.xiaohongshu.com/explore/{feed_id}"


async def post_comment(feed_id: str, content: str) -> dict:
    await open_page(FEED_URL.format(feed_id=feed_id))
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    ref = _must_find(snap, "找到评论输入框", "评论", "textbox")
    await click(ref)
    await fill(ref, content)
    await asyncio.sleep(0.5)

    snap2 = await snapshot("-i")
    send_ref = _find_ref(snap2, "发送", "button")
    if send_ref:
        await click(send_ref)

    return {"success": True, "message": "评论发表成功"}


async def reply_comment(feed_id: str, comment_id: str, content: str) -> dict:
    await open_page(FEED_URL.format(feed_id=feed_id))
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    ref = _must_find(snap, "找到回复按钮", "回复", "button")
    await click(ref)
    await asyncio.sleep(0.5)

    snap2 = await snapshot("-i")
    ref2 = _must_find(snap2, "找到回复输入框", "textbox")
    await fill(ref2, content)

    return {"success": True, "message": "评论回复成功"}
