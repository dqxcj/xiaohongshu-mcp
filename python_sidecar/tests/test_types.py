from python_sidecar.xhs.types import (
    PublishRequest, PublishVideoRequest, LoginStatus,
    QrcodeInfo, ApiResponse, FilterOptions,
)


def test_publish_request_defaults():
    req = PublishRequest(title="test", content="test", images=["a.png"])
    assert req.tags == []
    assert req.is_original is False
    assert req.visibility == "公开可见"


def test_login_status_defaults():
    status = LoginStatus(is_logged_in=True)
    assert status.username == ""


def test_qrcode_info():
    info = QrcodeInfo(timeout="240s", is_logged_in=False, img="base64...")
    assert info.timeout == "240s"


def test_api_response_ok():
    resp = ApiResponse(ok=True, data={"foo": "bar"})
    assert resp.ok is True
    assert resp.data["foo"] == "bar"


def test_api_response_err():
    resp = ApiResponse(ok=False, error="browser_error", message="Chrome crashed")
    assert resp.ok is False
    assert resp.error == "browser_error"
