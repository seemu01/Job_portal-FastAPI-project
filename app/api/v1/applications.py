from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)
from app.models.application import Application, ApplicationStatus
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


# =========================
# USER applies to a job
# =========================
@router.post("/", response_model=ApplicationResponse)
def apply_to_job(
    data: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.USER])),
):
    job = db.query(Job).filter(
        Job.id == data.job_id,
        Job.is_active == True
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    application = Application(
        user_id=current_user.id,
        job_id=data.job_id,
    )

    db.add(application)

    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="You already applied to this job"
        )

    db.refresh(application)

    return {
        "id": application.id,
        "job_id": application.job_id,
        "status": application.status,
        "notes": application.notes,
        "applied_at": application.applied_at,
        "updated_at": application.updated_at,
        "applicant_email": current_user.email,
    }


# =========================
# USER views their applications
# =========================
@router.get("/me", response_model=List[ApplicationResponse])
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.USER])),
):
    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).all()

    response = []

    for app in applications:
        response.append({
            "id": app.id,
            "job_id": app.job_id,
            "status": app.status,
            "notes": app.notes,
            "applied_at": app.applied_at,
            "updated_at": app.updated_at,
            "applicant_email": current_user.email,
        })

    return response


# RECRUITER views applications for their job
@router.get("/job/{job_id}", response_model=List[ApplicationResponse])
def applications_for_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.RECRUITER])),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job or job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    applications = db.query(Application).filter(
        Application.job_id == job_id
    ).all()

    response = []

    for app in applications:
        response.append({
            "id": app.id,
            "job_id": app.job_id,
            "status": app.status,
            "notes": app.notes,
            "applied_at": app.applied_at,
            "updated_at": app.updated_at,
            "applicant_email": app.user.email,
        })

    return response


# RECRUITER updates application status
@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application_status(
    application_id: int,
    data: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.RECRUITER])),
):
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    job = db.query(Job).filter(Job.id == application.job_id).first()

    if not job or job.recruiter_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # Normalize enum values safely
    current_status = ApplicationStatus(application.status)
    requested_status = ApplicationStatus(data.status)

    allowed_transitions = {
        ApplicationStatus.APPLIED: [
            ApplicationStatus.SHORTLISTED,
            ApplicationStatus.REJECTED
        ],
        ApplicationStatus.SHORTLISTED: [
            ApplicationStatus.HIRED,
            ApplicationStatus.REJECTED
        ],
        ApplicationStatus.REJECTED: [],
        ApplicationStatus.HIRED: []
    }

    if requested_status not in allowed_transitions[current_status]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status transition"
        )

    application.status = requested_status

    if data.notes is not None:
        application.notes = data.notes

    db.commit()
    db.refresh(application)

    return {
        "id": application.id,
        "job_id": application.job_id,
        "status": application.status,
        "notes": application.notes,
        "applied_at": application.applied_at,
        "updated_at": application.updated_at,
        "applicant_email": application.user.email,
    }
    if application.status == ApplicationStatus.HIRED:
        response["message"] = "Congratulations! You have been selected. Let's begin the journey 🎉"
    elif application.status ==ApplicationStatus.REJECTED:
        response["message"]="Better luck next time..keep improving have a nice day "
    else:
        response["message"]="Don't loose hope.. Jai sri RadhaKrishna "
    return response