from fastapi import APIRouter, HTTPException

from app.models.schemas import JobResponse
from app.services.job_service import JobService


router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"]
)

service = JobService()


@router.get(
    "",
    response_model=list[JobResponse]
)
def get_all_jobs():
    return service.get_all_jobs()


@router.get(
    "/{job_title}",
    response_model=JobResponse
)
def get_job(job_title: str):

    job = service.get_job(job_title)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail=f"Job '{job_title}' not found"
        )

    return job