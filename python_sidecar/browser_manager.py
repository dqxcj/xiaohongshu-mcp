import asyncio
import logging

logger = logging.getLogger(__name__)


class BrowserManager:
    def __init__(self):
        self._browser = None
        self._context = None

    async def start(self):
        """Launch CloakBrowser once, reuse across operations."""
        from cloakbrowser import launch_async

        logger.info("Launching CloakBrowser...")
        self._browser = await launch_async(
            headless=True,
            humanize=True,
            args=[
                "--remote-debugging-port=9222",
                "--no-first-run",
                "--no-default-browser-check",
            ],
        )
        self._context = self._browser.contexts[0] if self._browser.contexts else None
        logger.info("CloakBrowser launched with humanize=True")

    async def new_page(self):
        """Open a new tab."""
        if not self._context:
            self._context = self._browser.contexts[0]
        return await self._context.new_page()

    async def stop(self):
        if self._browser:
            logger.info("Shutting down CloakBrowser...")
            await self._browser.close()
            self._browser = None
            self._context = None

    @property
    def browser(self):
        return self._browser


_browser_manager: BrowserManager | None = None


def get_browser_manager() -> BrowserManager:
    if _browser_manager is None:
        raise RuntimeError("BrowserManager not started. Call start() first.")
    return _browser_manager


async def init_browser():
    global _browser_manager
    _browser_manager = BrowserManager()
    await _browser_manager.start()


async def shutdown_browser():
    global _browser_manager
    if _browser_manager:
        await _browser_manager.stop()
        _browser_manager = None
