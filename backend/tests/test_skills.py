from fastapi.testclient import TestClient

from app.main import app
from app.routes import skills


client = TestClient(app)


def test_get_skill(monkeypatch):

    def mock_get_skill(skill_name):
        return {
            "name": "Python",
            "description": "General-purpose programming language",
            "difficulty": "Beginner",
        }

    monkeypatch.setattr(
        skills.service,
        "get_skill",
        mock_get_skill,
    )

    response = client.get("/api/skills/Python")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Python"
    assert data["difficulty"] == "Beginner"


def test_get_skill_not_found(monkeypatch):

    def mock_get_skill(skill_name):
        return None

    monkeypatch.setattr(
        skills.service,
        "get_skill",
        mock_get_skill,
    )

    response = client.get("/api/skills/Unknown")

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Skill 'Unknown' not found"
    )


def test_get_related_skills(monkeypatch):

    def mock_get_skill(skill_name):
        return {
            "name": "Python",
            "description": "General-purpose programming language",
            "difficulty": "Beginner",
        }

    def mock_get_related_skills(skill_name):
        return [
            {
                "name": "FastAPI",
                "description": "Python framework for building APIs",
                "difficulty": "Intermediate",
            }
        ]

    monkeypatch.setattr(
        skills.service,
        "get_skill",
        mock_get_skill,
    )

    monkeypatch.setattr(
        skills.service,
        "get_related_skills",
        mock_get_related_skills,
    )

    response = client.get(
        "/api/skills/Python/related"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "FastAPI"


def test_get_recommendations(monkeypatch):

    def mock_get_skill(skill_name):
        return {
            "name": "Python",
            "description": "General-purpose programming language",
            "difficulty": "Beginner",
        }

    def mock_get_recommendations(skill_name):
        return [
            {
                "skill": "FastAPI",
                "description": "Python framework for building APIs",
                "difficulty": "Intermediate",
                "careers": [
                    "Backend Developer",
                    "Full Stack Developer",
                ],
            }
        ]

    monkeypatch.setattr(
        skills.service,
        "get_skill",
        mock_get_skill,
    )

    monkeypatch.setattr(
        skills.service,
        "get_recommendations",
        mock_get_recommendations,
    )

    response = client.get(
        "/api/skills/Python/recommendations"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["skill"] == "Python"
    assert len(data["recommendations"]) == 1
    assert (
        data["recommendations"][0]["skill"]
        == "FastAPI"
    )


def test_get_learning_path(monkeypatch):

    def mock_get_skill(skill_name):
        return {
            "name": "Python",
            "description": "General-purpose programming language",
            "difficulty": "Beginner",
        }

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
        skills.service,
        "get_skill",
        mock_get_skill,
    )

    monkeypatch.setattr(
        skills.service,
        "get_learning_path",
        mock_get_learning_path,
    )

    response = client.get(
        "/api/skills/Python/learning-path/ML%20Engineer"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["skill"] == "Python"
    assert data["job"] == "ML Engineer"
    assert data["distance"] == 2

    assert data["path"][0]["name"] == "Python"
    assert data["path"][1]["name"] == "Machine Learning"
    assert data["path"][2]["name"] == "ML Engineer"


def test_learning_path_not_found(monkeypatch):

    def mock_get_skill(skill_name):
        return {
            "name": "Python",
            "description": "General-purpose programming language",
            "difficulty": "Beginner",
        }

    def mock_get_learning_path(
        skill_name,
        job_name,
    ):
        return None

    monkeypatch.setattr(
        skills.service,
        "get_skill",
        mock_get_skill,
    )

    monkeypatch.setattr(
        skills.service,
        "get_learning_path",
        mock_get_learning_path,
    )

    response = client.get(
        "/api/skills/Python/learning-path/Unknown%20Job"
    )

    assert response.status_code == 404

    assert "No learning path found" in (
        response.json()["detail"]
    )