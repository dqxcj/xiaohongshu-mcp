import asyncio
import logging
from python_sidecar.agent_browser import run, open_page, snapshot, fill

logger = logging.getLogger(__name__)

HOME_URL = "https://creator.xiaohongshu.com"


async def list_feeds() -> list[dict]:
    await open_page(HOME_URL)
    await asyncio.sleep(3)

    feeds = []
    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "link" in line.lower() and "card" in line.lower():
            feeds.append({"title": line})
    return feeds


async def search_feeds(keyword: str, sort_by: str = "综合",
                       note_type: str = "不限", publish_time: str = "不限",
                       search_scope: str = "不限", location: str = "不限") -> list[dict]:
    await open_page(f"{HOME_URL}/search")
    await asyncio.sleep(2)

    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "搜索" in line and "textbox" in line.lower():
            ref = line.split("[ref=")[-1].rstrip("]")
            await fill(ref, keyword)
            await asyncio.sleep(0.5)
            await run("press", "Enter")
            break
    await asyncio.sleep(3)

    feeds = []
    snap = await snapshot("-i")
    for line in snap.split("\n"):
        if "link" in line.lower() and ("card" in line.lower() or "note" in line.lower()):
            feeds.append({"title": line})
    return feeds
