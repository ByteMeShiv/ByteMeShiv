from httpx import AsyncClient

async def get_http_client():
    async with AsyncClient(timeout=10) as client:
        yield client