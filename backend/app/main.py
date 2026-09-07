from fastapi import FastAPI, status
from backend.app.routes.jobs import router as jobs_router

app = FastAPI()
app.include_router(jobs_router)

@app.get("/")
async def read_root():
    return {"message" : "ApplyPilot AI API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

