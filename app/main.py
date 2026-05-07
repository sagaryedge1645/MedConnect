from fastapi import FastAPI
from app.core.database import Base,engine
import app.models
from app.api import api_router

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Backend running"}