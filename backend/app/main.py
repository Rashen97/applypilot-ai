from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()
class JobCreate(BaseModel):
    title: str
    company: str

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

@app.get("/")
async def read_root():
    return {"message" : "ApplyPilot AI API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/jobs")
async def get_jobs():
    return jobs

@app.post("/jobs", status_code=status.HTTP_201_CREATED)
async def create_job(job: JobCreate):
    new_job = {
        "id": len(jobs) + 1,
        "title": job.title,
        "company": job.company,
    }
    jobs.append(new_job)
    return new_job