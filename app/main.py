from fastapi import FastAPI
from app.routers import videos

app = FastAPI

app.include_router(videos.router)

@app.get('/')
def root():
    return {'massage': 'Hellow World'}