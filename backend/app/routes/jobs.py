# Contains job related API endpoints
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session 

from backend.app.schemas.job import JobCreate, JobUpdate, JobResponse
from backend.app.database import get_db
from backend.app.models.job import Job


router = APIRouter()

@router.get("/jobs", response_model=list[JobResponse])
async def get_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    return job

@router.patch("/jobs/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    update_data = job_update.dict(exclude_unset=True)  # get only the fields that were provided in the request
    for field, value in update_data.items():
        setattr(job, field, value)  # update the job object with the new values

    db.commit()
    db.refresh(job)

    return job

@router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job: JobCreate,
    db: Session = Depends(get_db)
):
    new_job = Job(title=job.title, company=job.company)

    db.add(new_job)
    db.commit()          # finalize the changes made to the database
    db.refresh(new_job)  # reload this object from the database to get the updated values (like id)

    return new_job

@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    db.delete(job)
    db.commit()
