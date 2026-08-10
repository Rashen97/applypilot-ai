from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message" : "ApplyPilot AI API is running"}