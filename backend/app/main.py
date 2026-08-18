from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.neo4j import verify_database_connection
from app.routes.skills import router as skills_router
from app.routes.jobs import router as jobs_router


app = FastAPI(
    title="TechPath API",
    description="Career and skill graph powered by CognoDB",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
        "https://techpath-frontend-qnrm.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(skills_router)
app.include_router(jobs_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to TechPath API"
    }


@app.get("/health")
def health():
    try:
        verify_database_connection()

        return {
            "status": "ok",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "error",
            "database": "unavailable"
        }