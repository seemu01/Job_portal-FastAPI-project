from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum
from datetime import datetime


class ApplicationStatus(enum.Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"
    HIRED = "HIRED"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), index=True)

    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.APPLIED
    )

    notes = Column(Text, nullable=True)

    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # 🔥 RELATIONSHIPS (IMPORTANT)
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")

    # Prevent duplicate applications
    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="unique_user_job"),
    )
