from pydantic import BaseModel
from typing import Optional


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = "No description provided."
    stack: Optional[str] = "N/A"
    url: str
    stars: int = 0