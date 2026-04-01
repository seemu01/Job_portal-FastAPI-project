from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    description: str
    location: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None


class JobUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    location: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    is_active: Optional[bool]


class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    location: str
    salary_min: Optional[int]
    salary_max: Optional[int]
    recruiter_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
