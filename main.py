from fastapi import FastAPI
from app.routes.github import router as github_router
from app.services.cron import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(github_router, prefix="/api/v1/github",tags=["Github"])

@app.get("/",tags=["Init"])
async def health():
    return {"message": "hello from galaxy"}