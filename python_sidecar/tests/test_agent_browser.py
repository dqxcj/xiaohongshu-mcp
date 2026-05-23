import pytest
from unittest.mock import AsyncMock, patch
from python_sidecar.agent_browser import open_page, snapshot, click, fill, upload, scroll


@pytest.mark.asyncio
async def test_open_page_calls_run_with_open():
    with patch("python_sidecar.agent_browser.run", new_callable=AsyncMock) as mock_run:
        await open_page("https://example.com")
        mock_run.assert_called_once_with("open", "https://example.com")


@pytest.mark.asyncio
async def test_click_calls_run_with_click_and_ref():
    with patch("python_sidecar.agent_browser.run", new_callable=AsyncMock) as mock_run:
        await click("@e5")
        mock_run.assert_called_once_with("click", "@e5")


@pytest.mark.asyncio
async def test_fill_calls_run_with_fill_ref_and_text():
    with patch("python_sidecar.agent_browser.run", new_callable=AsyncMock) as mock_run:
        await fill("@e3", "hello")
        mock_run.assert_called_once_with("fill", "@e3", "hello")


@pytest.mark.asyncio
async def test_upload_calls_run_with_upload_ref_and_path():
    with patch("python_sidecar.agent_browser.run", new_callable=AsyncMock) as mock_run:
        await upload("@e12", "/tmp/img.png")
        mock_run.assert_called_once_with("upload", "@e12", "/tmp/img.png")


@pytest.mark.asyncio
async def test_scroll_defaults_to_down():
    with patch("python_sidecar.agent_browser.run", new_callable=AsyncMock) as mock_run:
        await scroll()
        mock_run.assert_called_once_with("scroll", "down")


@pytest.mark.asyncio
async def test_snapshot_passes_args():
    with patch("python_sidecar.agent_browser.run", new_callable=AsyncMock) as mock_run:
        await snapshot("-i")
        mock_run.assert_called_once_with("snapshot", "-i")
