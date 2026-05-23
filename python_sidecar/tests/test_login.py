import pytest
from python_sidecar.conftest import SAMPLE_LOGGED_IN_SNAPSHOT, SAMPLE_LOGGED_OUT_SNAPSHOT
from python_sidecar.xhs.login import check_login_status, delete_cookies


@pytest.mark.asyncio
async def test_check_login_status_logged_in(mock_agent_browser):
    mock_agent_browser["snapshot"].return_value = SAMPLE_LOGGED_IN_SNAPSHOT
    result = await check_login_status()
    assert result.is_logged_in is True
    assert result.username == "小红书创作者"


@pytest.mark.asyncio
async def test_check_login_status_logged_out(mock_agent_browser):
    mock_agent_browser["snapshot"].return_value = SAMPLE_LOGGED_OUT_SNAPSHOT
    result = await check_login_status()
    assert result.is_logged_in is False


@pytest.mark.asyncio
async def test_delete_cookies(mock_agent_browser):
    result = await delete_cookies()
    assert result is None
