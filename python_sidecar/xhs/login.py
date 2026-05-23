import asyncio
import logging
from python_sidecar.agent_browser import run, open_page, snapshot, screenshot
from python_sidecar.xhs.types import LoginStatus, QrcodeInfo

logger = logging.getLogger(__name__)

XHS_CREATOR_URL = "https://creator.xiaohongshu.com"


async def check_login_status() -> LoginStatus:
    await open_page(XHS_CREATOR_URL)
    await asyncio.sleep(3)
    snap = await snapshot("-i")

    if "发布图文" in snap or "创作中心" in snap:
        return LoginStatus(is_logged_in=True, username="小红书创作者")
    return LoginStatus(is_logged_in=False)


async def get_login_qrcode() -> QrcodeInfo:
    await open_page(f"{XHS_CREATOR_URL}/login")
    await asyncio.sleep(3)
    snap = await snapshot("-i")

    for line in snap.split("\n"):
        if "img" in line.lower() and ("qrcode" in line.lower() or "二维码" in line):
            ref = line.split("[ref=")[-1].rstrip("]")
            return QrcodeInfo(timeout="240s", is_logged_in=False, img="")

    await screenshot("/tmp/xhs_qrcode.png")
    return QrcodeInfo(timeout="240s", is_logged_in=False, img="/tmp/xhs_qrcode.png")


async def delete_cookies():
    import os
    import shutil
    profile_dir = "./browser_profile"
    if os.path.exists(profile_dir):
        shutil.rmtree(profile_dir)
