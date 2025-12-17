from httpx import AsyncClient

class ProjectService():
    def __init__(self,client : AsyncClient) -> None:
        self.client = client

    async def get_projects(self):
        resp = await self.client.get("")
        resp.raise_for_status()
        resp.json()
        return resp
