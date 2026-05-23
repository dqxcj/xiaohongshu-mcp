import asyncio


async def run(*args: str, timeout: float = 30.0) -> str:
    """Run an agent-browser command and return stdout."""
    cmd = ["agent-browser"] + list(args)
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
