from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from backend.config import settings
from backend.dependency import get_project_service
from backend.services.project import ProjectService
from backend.services.project_cache import project_cache

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/projects", name='read_projects')
async def read_projects(
    request: Request, 
    service: ProjectService = Depends(get_project_service)
):
    try:
        projects = await service.get_all_projects()
        return templates.TemplateResponse("project.html", {"request": request, "projects": projects})
    except Exception:
        return templates.TemplateResponse("project.html", {
            "request": request, 
            "projects": project_cache.data,
            "error": "Live update failed, showing cached data."
        })

@router.get("/project/{id}", name='read_project')
async def read_project(
    id: int, 
    request: Request, 
    service: ProjectService = Depends(get_project_service)
):
    try:
        data = await service.get_project_by_id(id)
        # Verify ownership
        if data.get("owner", {}).get("login", "").lower() != settings.GITHUB_USERNAME.lower():
            raise HTTPException(status_code=404, detail="Project not found")
            
        return templates.TemplateResponse("detail.html", {"request": request, "project": data})
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=503, detail="Service Unavailable")