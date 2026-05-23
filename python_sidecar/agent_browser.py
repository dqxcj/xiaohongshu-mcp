import asyncio
import os
import platform
import sys


def _find_agent_browser():
    """Auto-detect the agent-browser binary path."""
    env_path = os.environ.get("AGENT_BROWSER_BIN")
    if env_path:
        return env_path

    npm_roots = []
    if sys.platform == "win32":
        npm_roots = [
            os.path.expandvars(r"%APPDATA%\npm"),
            r"D:\ProgramFiles\nodejs",
            r"C:\Program Files\nodejs",
        ]
    else:
        npm_roots = ["/usr/local/bin", os.path.expanduser("~/.npm-global/bin")]

    binary_name = "agent-browser" + (".exe" if sys.platform == "win32" else "")
    for root in npm_roots:
        path = os.path.join(root, binary_name)
        if os.path.exists(path):
            return path
        inner = os.path.join(root, "node_modules", "agent-browser", "bin")
        if os.path.isdir(inner):
            mapping = {
                "win32": "agent-browser-win32-x64.exe",
                "linux": f"agent-browser-linux-{platform.machine()}",
                "darwin": f"agent-browser-darwin-{platform.machine()}",
            }
            binary = mapping.get(sys.platform)
            if binary:
                bin_path = os.path.join(inner, binary)
                if os.path.exists(bin_path):
                    return bin_path
            js_path = os.path.join(inner, "agent-browser.js")
            if os.path.exists(js_path):
                return js_path

    return binary_name


_AGENT_BROWSER_BIN = _find_agent_browser()


async def run(*args: str, timeout: float = 30.0) -> str:
    """Run an agent-browser command and return stdout.

    All commands route through port 9222 (CloakBrowser) for stealth.
    """
    cmd = [_AGENT_BROWSER_BIN] + list(args)
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout
        )
    except asyncio.TimeoutError:
        proc.kill()
        raise RuntimeError(f"agent-browser timed out after {timeout}s: {' '.join(cmd)}")

    if proc.returncode != 0:
        raise RuntimeError(
            f"agent-browser exited {proc.returncode}: {' '.join(cmd)}\n{stderr.decode()}"
        )
    return stdout.decode().strip()


async def open_page(url: str) -> str:
    return await run("open", url)


async def snapshot(*args: str) -> str:
    return await run("snapshot", *args)


async def click(ref: str) -> str:
    return await run("click", ref)


async def fill(ref: str, text: str) -> str:
    return await run("fill", ref, text)


async def type_text(ref: str, text: str) -> str:
    return await run("type", ref, text)


async def upload(ref: str, path: str) -> str:
    return await run("upload", ref, path)


async def screenshot(path: str) -> str:
    return await run("screenshot", path)


async def get_text(ref: str) -> str:
    return await run("get", "text", ref)


async def scroll(direction: str = "down") -> str:
    return await run("scroll", direction)
