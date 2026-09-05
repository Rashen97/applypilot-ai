from pydantic import BaseModel
from fastapi import status

# in models we have the job description and thats why have these data

class JobCreate(BaseModel):
    title: str
    company: str

