from fastapi import FastAPI
from .settings import Settings

app = FastAPI(
    title=Settings.NAME,
    description=Settings.DESCRIPTION,
)

@app.get("/")
def root():
    return {"message": "Welcome to the Bank API"}