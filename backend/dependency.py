from httpx import AsyncClient
from fastapi import Depends
from backend.services.project import ProjectService

async def get_http_client():
    async with AsyncClient(timeout=10) as client:
        yield client

async def get_project_service(client: AsyncClient = Depends(get_http_client)):
    return ProjectService(client)