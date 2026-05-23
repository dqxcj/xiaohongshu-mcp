import asyncio
import logging
from python_sidecar.agent_browser import (
    run, open_page, snapshot, click, fill, upload,
)
from python_sidecar.xhs.types import PublishRequest

logger = logging.getLogger(__name__)

PUBLISH_URL = "https://creator.xiaohongshu.com/publish/publish?source=official"


def _find_ref(snap: str, *keywords: str) -> str | None:
    """Find element ref by matching ALL keywords in a snapshot line."""
    for line in snap.split("\n"):
        if all(kw in line for kw in keywords):
            return line.split("[ref=")[-1].rstrip("]")
    return None


def _must_find(snap: str, step: str, *keywords: str) -> str:
    ref = _find_ref(snap, *keywords)
    if ref is None:
        raise RuntimeError(f"{step}: 未在页面中找到匹配元素 (keywords={keywords})")
    return ref


async def publish_content(req: PublishRequest) -> dict:
    await open_page(PUBLISH_URL)
    await asyncio.sleep(3)

    snap = await snapshot("-i")
    ref = _must_find(snap, "选择图文Tab", "上传图文")
    await click(ref)
    await asyncio.sleep(2)

    for i, img_path in enumerate(req.images):
        snap = await snapshot("-i")
        ref = _must_find(snap, f"上传图片{i+1}", "upload")
        await upload(ref, img_path)
        await asyncio.sleep(1)

    snap = await snapshot("-i")
    ref = _must_find(snap, "填写标题", "标题", "textbox")
    await fill(ref, req.title)

    snap = await snapshot("-i")
    ref = _must_find(snap, "填写正文", "正文", "textbox")
    await fill(ref, req.content)

    for tag in req.tags[:10]:
        snap = await snapshot("-i")
        tag_ref = _find_ref(snap, "添加话题")
        if tag_ref is None:
            logger.warning(f"未找到添加话题按钮，跳过标签: {tag}")
            break
        await click(tag_ref)
        await asyncio.sleep(0.5)
        snap = await snapshot("-i")
        ref = _find_ref(snap, "textbox")
        if ref is None:
            logger.warning(f"未找到标签输入框，跳过标签: {tag}")
            break
        await fill(ref, tag)
        await asyncio.sleep(0.5)

    snap = await snapshot("-i")
    ref = _must_find(snap, "点击发布按钮", "发布", "button")
    await click(ref)

    await asyncio.sleep(3)
    return {"status": "发布完成", "post_id": ""}
