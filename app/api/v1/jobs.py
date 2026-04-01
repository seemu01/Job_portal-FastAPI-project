from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.models.job import Job
from app.models.user import User, UserRole
from app.api.deps import require_role

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE JOB (Recruiter Only)
@router.post("/", response_model=JobResponse)
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.RECRUITER])),
):
    job = Job(
        **job_data.dict(),
        recruiter_id=current_user.id,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


# LIST ALL ACTIVE JOBS (Public)
@router.get("/", response_model=List[JobResponse])
def list_jobs(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    offset = (page - 1) * limit

    return (
        db.query(Job)
        .filter(Job.is_active == True)
        .order_by(Job.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


# LIST RECRUITER'S OWN JOBS
@router.get("/my", response_model=List[JobResponse])
def my_jobs(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.RECRUITER])),
):
    offset = (page - 1) * limit

    return (
        db.query(Job)
        .filter(
            Job.recruiter_id == current_user.id,
            Job.is_active == True
        )
        .order_by(Job.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


# UPDATE JOB (Owner Only)
@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.RECRUITER])),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    for field, value in job_data.dict(exclude_unset=True).items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)
    return job
