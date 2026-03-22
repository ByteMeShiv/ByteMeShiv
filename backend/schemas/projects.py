from pydantic import BaseModel
from typing import Optional, List

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = "No description provided."
    stack: Optional[str] = "N/A"
    topics: List[str] = []  # Added topics array
    url: str
    stars: int = 0
    forks: int = 0          # Added forks count