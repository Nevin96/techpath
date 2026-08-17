from app.services.graph_service import GraphService


def test_get_skill(monkeypatch):

    service = GraphService()

    def mock_get_skill(skill_name):
        return {
            "name": "Python",
            "description": "General-purpose programming language",
            "difficulty": "Beginner",
        }

    monkeypatch.setattr(
        service.repository,
        "get_skill",
        mock_get_skill,
    )

    result = service.get_skill("Python")

    assert result["name"] == "Python"
    assert result["difficulty"] == "Beginner"


def test_get_related_skills(monkeypatch):

    service = GraphService()

    def mock_get_related_skills(skill_name):
        return [
            {
                "name": "FastAPI",
                "description": "Python framework for building APIs",
                "difficulty": "Intermediate",
            }
        ]

    monkeypatch.setattr(
        service.repository,
        "get_related_skills",
        mock_get_related_skills,
    )

    result = service.get_related_skills("Python")

    assert len(result) == 1
    assert result[0]["name"] == "FastAPI"


def test_get_recommendations(monkeypatch):

    service = GraphService()

    def mock_get_recommendations(skill_name):
        return [
            {
                "skill": "FastAPI",
                "description": "Python framework for building APIs",
                "difficulty": "Intermediate",
                "careers": [
                    "Backend Developer"
                ],
            }
        ]

    monkeypatch.setattr(
        service.repository,
        "get_recommendations",
        mock_get_recommendations,
    )

    result = service.get_recommendations("Python")

    assert len(result) == 1
    assert result[0]["skill"] == "FastAPI"


def test_get_learning_path(monkeypatch):

    service = GraphService()

    def mock_get_learning_path(
        skill_name,
        job_name,
    ):
        return {
            "skill": "Python",
            "job": "ML Engineer",
            "path": [
                {
                    "name": "Python",
                    "type": "skill",
                    "description": "General-purpose programming language",
                    "difficulty": "Beginner",
                },
                {
                    "name": "Machine Learning",
                    "type": "skill",
                    "description": "Methods for building systems that learn from data",
                    "difficulty": "Advanced",
                },
                {
                    "name": "ML Engineer",
                    "type": "job",
                    "description": "Build and deploy machine learning systems",
                    "difficulty": None,
                },
            ],
            "distance": 2,
        }

    monkeypatch.setattr(
        service.repository,
        "get_learning_path",
        mock_get_learning_path,
    )

    result = service.get_learning_path(
        "Python",
        "ML Engineer",
    )

    assert result["skill"] == "Python"
    assert result["job"] == "ML Engineer"
    assert result["distance"] == 2
    assert result["path"][0]["name"] == "Python"
    assert result["path"][-1]["name"] == "ML Engineer"