# Contains job related API endpoints
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session 

from backend.app.schemas.job import JobCreate
from backend.app.database import get_db
from backend.app.models.job import Job


router = APIRouter()

@router.get("/jobs")
async def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

@router.post("/jobs", status_code=status.HTTP_201_CREATED)
async def create_job(
    job: JobCreate,
    db: Session = Depends(get_db)
):
    new_job = Job(title=job.title, company=job.company)

    db.add(new_job)
    db.commit()          # finalize the changes made to the database
    db.refresh(new_job)  # reload this object from the database to get the updated values (like id)

    return new_job