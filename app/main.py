from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Music Feature Engine")
app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Music Feature Engine is up"}