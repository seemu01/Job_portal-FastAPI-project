from fastapi import FastAPI
from app.core.database import engine, Base

# Import models so SQLAlchemy knows about them
from app.models import user, job, application

from app.api.v1 import auth, users, jobs, applications

app = FastAPI()


@app.on_event("startup")
def startup_event():
    # Test DB connection
    try:
        with engine.connect() as connection:
            print("✅ Database connected successfully")
    except Exception as e:
        print("❌ Database connection failed:", e)

    # Create tables if not exist
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(
    applications.router,
    prefix="/api/v1/applications",
    tags=["Applications"],
)


@app.get("/")
def root():
    return {"status": "Job Portal API running 🚀"}
