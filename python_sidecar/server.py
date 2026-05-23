import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from python_sidecar.browser_manager import init_browser, shutdown_browser
from python_sidecar.xhs.types import PublishRequest, PublishVideoRequest
from python_sidecar.xhs import login, publish, publish_video, feeds
from python_sidecar.xhs import feed_detail, comment, like_favorite, user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_browser()
    yield
    await shutdown_browser()


app = FastAPI(title="xiaohongshu-sidecar", lifespan=lifespan)


def ok(data: dict | None = None) -> dict:
    return {"ok": True, "data": data}


def err(error: str, message: str = "") -> dict:
    return {"ok": False, "error": error, "message": message}


@app.post("/login/status")
async def login_status():
    try:
        result = await login.check_login_status()
        return ok({"is_logged_in": result.is_logged_in, "username": result.username})
    except Exception as e:
        return err("login_error", str(e))


@app.post("/login/qrcode")
async def login_qrcode():
    try:
        result = await login.get_login_qrcode()
        return ok({"timeout": result.timeout, "is_logged_in": result.is_logged_in, "img": result.img})
    except Exception as e:
        return err("qrcode_error", str(e))


@app.delete("/login/cookies")
async def login_cookies():
    try:
        await login.delete_cookies()
        return ok()
    except Exception as e:
        return err("cookies_error", str(e))


@app.post("/publish")
async def publish_endpoint(req: PublishRequest):
    try:
        result = await publish.publish_content(req)
        return ok(result)
    except Exception as e:
        return err("publish_error", str(e))


@app.post("/publish_video")
async def publish_video_endpoint(req: PublishVideoRequest):
    try:
        result = await publish_video.publish_video(req)
        return ok(result)
    except Exception as e:
        return err("publish_video_error", str(e))


@app.get("/feeds/list")
async def feeds_list():
    try:
        result = await feeds.list_feeds()
        return ok({"feeds": result, "count": len(result)})
    except Exception as e:
        return err("feeds_error", str(e))


@app.post("/feeds/search")
async def feeds_search(req: dict):
    try:
        keyword = req.get("keyword", "")
        result = await feeds.search_feeds(keyword)
        return ok({"feeds": result, "count": len(result)})
    except Exception as e:
        return err("search_error", str(e))


@app.post("/feeds/detail")
async def feeds_detail(req: dict):
    try:
        feed_id = req.get("feed_id", "")
        load_all = req.get("load_all_comments", False)
        result = await feed_detail.get_feed_detail(feed_id, load_all)
        return ok(result)
    except Exception as e:
        return err("detail_error", str(e))


@app.post("/feeds/comment")
async def feeds_comment(req: dict):
    try:
        feed_id = req["feed_id"]
        content = req["content"]
        result = await comment.post_comment(feed_id, content)
        return ok(result)
    except Exception as e:
        return err("comment_error", str(e))


@app.post("/feeds/comment/reply")
async def feeds_comment_reply(req: dict):
    try:
        feed_id = req["feed_id"]
        comment_id = req.get("comment_id", "")
        content = req["content"]
        result = await comment.reply_comment(feed_id, comment_id, content)
        return ok(result)
    except Exception as e:
        return err("reply_error", str(e))


@app.post("/like")
async def like_endpoint(req: dict):
    try:
        feed_id = req["feed_id"]
        if req.get("unlike"):
            result = await like_favorite.unlike_feed(feed_id)
        else:
            result = await like_favorite.like_feed(feed_id)
        return ok(result)
    except Exception as e:
        return err("like_error", str(e))


@app.post("/favorite")
async def favorite_endpoint(req: dict):
    try:
        feed_id = req["feed_id"]
        if req.get("unfavorite"):
            result = await like_favorite.unfavorite_feed(feed_id)
        else:
            result = await like_favorite.favorite_feed(feed_id)
        return ok(result)
    except Exception as e:
        return err("favorite_error", str(e))


@app.post("/user/profile")
async def user_profile_endpoint(req: dict):
    try:
        user_id = req["user_id"]
        result = await user.get_user_profile(user_id)
        return ok(result)
    except Exception as e:
        return err("user_error", str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=18061)
