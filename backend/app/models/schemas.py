from pydantic import BaseModel


class SkillResponse(BaseModel):
    name: str
    description: str
    difficulty: str


class JobResponse(BaseModel):
    title: str
    description: str


class CareerPath(BaseModel):
    job: str
    path: list[str]
    distance: int


class CareerPathResponse(BaseModel):
    skill: str
    paths: list[CareerPath]
    
class GraphNode(BaseModel):
    id: str
    type: str
    description: str | None = None
    difficulty: str | None = None


class GraphEdge(BaseModel):
    source: str
    target: str
    relationship: str


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]

class SkillRecommendation(BaseModel):
    skill: str
    difficulty: str | None = None
    description: str | None = None
    careers: list[str]


class RecommendationResponse(BaseModel):
    skill: str
    recommendations: list[SkillRecommendation]

class CareerLearningPathResponse(BaseModel):
    skill: str
    job: str
    path: list[str]
    distance: int
class LearningPathNode(BaseModel):
    name: str
    type: str
    description: str | None = None
    difficulty: str | None = None


class CareerLearningPathResponse(BaseModel):
    skill: str
    job: str
    path: list[LearningPathNode]
    distance: int