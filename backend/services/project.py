from httpx import AsyncClient, HTTPStatusError
from backend.config import settings
from backend.schemas.projects import ProjectResponse
from .project_cache import project_cache

class ProjectService:
    def __init__(self, client: AsyncClient):
        self.client = client
        self.headers = {"User-Agent": "FastAPI-Portfolio-App"}

    async def get_all_projects(self):
        # 1. Check Cache
        if project_cache.is_valid() and project_cache.data:
            return project_cache.data

        # 2. Fetch from GitHub
        url = f"https://api.github.com/users/{settings.GITHUB_USERNAME}/repos"
        params = {"sort": "updated", "per_page": 9}
        
        resp = await self.client.get(url, params=params, headers=self.headers)
        resp.raise_for_status()
        data = resp.json()


        clean_projects = [
            ProjectResponse(
                id=repo["id"],
                name=repo["name"].replace("-", " ").title(),
                description=repo.get("description"),
                stack=repo.get("language"),
                url=repo["html_url"],
                stars=repo["stargazers_count"]
            )
            for repo in data if not repo.get("fork")
        ]

        project_cache.update(clean_projects)
        return clean_projects

    async def get_project_by_id(self, project_id: int):
        url = f"https://api.github.com/repositories/{project_id}"
        resp = await self.client.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()