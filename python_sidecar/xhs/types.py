from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ApiResponse:
    ok: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    message: Optional[str] = None


@dataclass
class PublishRequest:
    title: str
    content: str
    images: list[str]
    tags: list[str] = field(default_factory=list)
    schedule_at: Optional[str] = None
    is_original: bool = False
    visibility: str = "公开可见"
    products: list[str] = field(default_factory=list)


@dataclass
class PublishVideoRequest:
    title: str
    content: str
    video: str
    tags: list[str] = field(default_factory=list)
    schedule_at: Optional[str] = None
    visibility: str = "公开可见"
    products: list[str] = field(default_factory=list)


@dataclass
class FilterOptions:
    sort_by: str = "综合"
    note_type: str = "不限"
    publish_time: str = "不限"
    search_scope: str = "不限"
    location: str = "不限"


@dataclass
class LoginStatus:
    is_logged_in: bool
    username: str = ""


@dataclass
class QrcodeInfo:
    timeout: str
    is_logged_in: bool
    img: str = ""
