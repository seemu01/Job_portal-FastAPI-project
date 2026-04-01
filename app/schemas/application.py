from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"
    HIRED = "HIRED"


class ApplicationCreate(BaseModel):
    job_id: int


class ApplicationUpdate(BaseModel):
    status: ApplicationStatus
    notes:str | None=None

class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    status: ApplicationStatus
    notes: str | None
    applied_at: datetime
    updated_at: datetime
    applicant_email: str

    class Config:
        from_attributes = True
