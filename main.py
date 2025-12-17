import time
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, status, Request, HTTPException
from fastapi.templating import Jinja2Templates
from httpx import AsyncClient, HTTPStatusError
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

 
GITHUB_USERNAME = "bytemeshiv"


class Project(BaseModel):
    id: int
    name: str
    description: Optional[str] = "No description provided."
    stack: Optional[str] = "N/A"
    url: str
    stars: int = 0  

templates = Jinja2Templates(directory="templates")
app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/healthcheck")
def get_healthcheck():
    return {"detail": "App is Sliving", "status": status.HTTP_200_OK}

@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": "Shivam",
        "title": "Shivam's Portfolio",
        "status" : status.HTTP_200_OK
    })



class ProjectCache:
    def __init__(self):
        self.data = []
        self.last_fetched = 0
        self.cache_duration = 1800  

    def is_valid(self):
        return (time.time() - self.last_fetched) < self.cache_duration

    def update(self, data):
        self.data = data
        self.last_fetched = time.time()


project_cache = ProjectCache()


@app.get("/projects", name='read_projects') 
async def read_projects(request: Request):
    

    if project_cache.is_valid() and project_cache.data:
        print("⚡ Serving from Cache") # Debug log
        return templates.TemplateResponse("project.html", {
            "request": request, 
            "projects": project_cache.data
        })

    print("🔄 Fetching from GitHub API")
    headers = {"User-Agent": "FastAPI-Portfolio-App"}
    url = "https://api.github.com/users/bytemeshiv/repos"
    params = {"sort": "updated", "per_page": 10} 

    try:
        async with AsyncClient() as client:
            resp = await client.get(url, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            
            clean_projects = []
            for repo in data:
                if repo.get("fork") is True:
                    continue
                
                project_obj = Project(
                    id=repo["id"],
                    name=repo["name"].replace("-", " ").title(),
                    description=repo["description"],
                    stack=repo["language"], 
                    url=repo["html_url"],
                    stars=repo["stargazers_count"]
                )
                clean_projects.append(project_obj)

            project_cache.update(clean_projects)

            return templates.TemplateResponse("project.html", {
                "request": request, 
                "projects": clean_projects
            })
            
    except Exception as e:
       
        if project_cache.data:
            return templates.TemplateResponse("project.html", {
                "request": request, 
                "projects": project_cache.data,
                "error": "Live update failed, showing cached data."
            })
        raise HTTPException(status_code=503, detail="Service Unavailable")
   

@app.get("/project/{id}", name='read_project')
async def read_project(request: Request, id: int):
    url = f"https://api.github.com/repositories/{id}"
    headers = {"User-Agent": "FastAPI-Portfolio-App"}
    
    try:
        async with AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers=headers)

            if resp.status_code == 404:
                raise HTTPException(status_code=404, detail="Project not found")
            
            resp.raise_for_status()
            data = resp.json()
            
            repo_owner = data.get("owner", {}).get("login", "").lower()
            
            if repo_owner != GITHUB_USERNAME.lower():
                raise HTTPException(status_code=404, detail="Project not found")
            
            context = {"request": request, "project": data}
            return templates.TemplateResponse("detail.html", context=context)
            
    except HTTPStatusError as e:
        print(f"GitHub API Error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail="GitHub API Error")
    except Exception as e:
        # If it is already a HTTPException (like our 404 above), re-raise it
        if isinstance(e, HTTPException):
            raise e
        print(f"Internal Error: {e}")
        raise HTTPException(status_code=503, detail="Service Unavailable")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("base.html", {"request": request, "error": "Internal Error"}, status_code=500)