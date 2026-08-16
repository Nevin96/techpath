from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    SkillResponse,
    JobResponse,
    CareerPathResponse,
    GraphResponse,
    RecommendationResponse,
)
from app.services.graph_service import GraphService


router = APIRouter(
    prefix="/api/skills",
    tags=["Skills"]
)

service = GraphService()


@router.get(
    "",
    response_model=list[SkillResponse]
)
def get_all_skills():
    return service.get_all_skills()


@router.get(
    "/{skill_name}",
    response_model=SkillResponse
)
def get_skill(skill_name: str):

    skill = service.get_skill(skill_name)

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{skill_name}' not found"
        )

    return skill


@router.get(
    "/{skill_name}/related",
    response_model=list[SkillResponse]
)
def get_related_skills(skill_name: str):

    skill = service.get_skill(skill_name)

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{skill_name}' not found"
        )

    return service.get_related_skills(skill_name)


@router.get(
    "/{skill_name}/jobs",
    response_model=list[JobResponse]
)
def get_jobs_for_skill(skill_name: str):

    skill = service.get_skill(skill_name)

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{skill_name}' not found"
        )

    return service.get_jobs_for_skill(skill_name)


@router.get(
    "/{skill_name}/career-paths",
    response_model=CareerPathResponse
)
def get_career_paths(skill_name: str):

    skill = service.get_skill(skill_name)

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{skill_name}' not found"
        )

    return {
        "skill": skill_name,
        "paths": service.get_career_paths(skill_name)
    }
@router.get(
    "/{skill_name}/graph",
    response_model=GraphResponse
)
def get_graph(skill_name: str):

    skill = service.get_skill(skill_name)

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{skill_name}' not found"
        )

    return service.get_graph(skill_name)
@router.get(
    "/{skill_name}/recommendations",
    response_model=RecommendationResponse
)
def get_recommendations(skill_name: str):

    skill = service.get_skill(skill_name)

    if skill is None:
        raise HTTPException(
            status_code=404,
            detail=f"Skill '{skill_name}' not found"
        )

    recommendations = service.get_recommendations(
        skill_name
    )

    return {
        "skill": skill["name"],
        "recommendations": recommendations,
    }