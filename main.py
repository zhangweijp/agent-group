import uvicorn
from fastapi import FastAPI
from config import settings
from core.database import engine, Base
from routers import project_router

app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

app.include_router(project_router.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
