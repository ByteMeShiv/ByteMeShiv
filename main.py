import os
from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.routes.projects import router as project_router


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="Shivam's Portfolio")


app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Include Routers
app.include_router(project_router)

@app.get("/healthcheck")
def get_healthcheck():
    return {"detail": "App is Sliving", "status": status.HTTP_200_OK}

@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "name": "Shivam",
        "title": "Shivam's Portfolio"
    })


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("base.html", {"request": request, "error": str(exc.detail)}, status_code=500)