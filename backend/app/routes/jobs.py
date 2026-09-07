# Contains job related API endpoints
from fastapi import APIRouter, status
from backend.app.models.job import JobCreate

router = APIRouter()

jobs = [
    {
        "id": 1,
        "title": "Graduate Software Engineer",
        "company": "Monzo",
    },
    {
        "id": 2,
        "title": "Python Developer",
        "company": "Example Technologies",
    },
    {
        "id": 3,
        "title": "Backend Engineer",
        "company": "Tech Startup",
    },
]

@router.get("/jobs")
async def get_jobs():
    return jobs

@router.post("/jobs", status_code=status.HTTP_201_CREATED)
async def create_job(job: JobCreate):
    new_job = {
        "id": len(jobs) + 1,
        "title": job.title,
        "company": job.company,
    }
    jobs.append(new_job)
    return new_job