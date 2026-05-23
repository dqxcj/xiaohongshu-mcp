import asyncio
import logging
from python_sidecar.agent_browser import open_page, snapshot, scroll

logger = logging.getLogger(__name__)

USER_URL = "https://www.xiaohongshu.com/user/profile/{user_id}"


async def get_user_profile(user_id: str) -> dict:
    await open_page(USER_URL.format(user_id=user_id))
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    await scroll("down")

    return {
        "user_id": user_id,
        "snapshot": snap,
    }
