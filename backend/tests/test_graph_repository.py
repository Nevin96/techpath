from app.repositories.graph_repository import GraphRepository


class FakeRecord:

    def __init__(self, data):
        self._data = data

    def data(self):
        return self._data

    def __getitem__(self, key):
        return self._data[key]


class FakeResult:

    def __init__(self, records):
        self.records = [
            FakeRecord(record)
            for record in records
        ]

    def __iter__(self):
        return iter(self.records)

    def single(self):
        if not self.records:
            return None

        return self.records[0]


class FakeSession:

    def __init__(self, responses):
        self.responses = responses
        self.queries = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def run(self, query, **parameters):

        self.queries.append({
            "query": query,
            "parameters": parameters,
        })

        return FakeResult(
            self.responses.pop(0)
        )


class FakeDriver:

    def __init__(self, responses):
        self.responses = responses
        self.session_instance = None

    def session(self, database=None):

        self.session_instance = FakeSession(
            self.responses
        )

        return self.session_instance


def test_get_skill(monkeypatch):

    fake_driver = FakeDriver([
        [
            {
                "name": "Python",
                "description": "General-purpose programming language",
                "difficulty": "Beginner",
            }
        ]
    ])

    monkeypatch.setattr(
        "app.repositories.graph_repository.get_driver",
        lambda: fake_driver,
    )

    repository = GraphRepository()

    result = repository.get_skill("Python")

    assert result is not None
    assert result["name"] == "Python"
    assert result["difficulty"] == "Beginner"


def test_get_related_skills(monkeypatch):

    fake_driver = FakeDriver([
        [
            {
                "name": "FastAPI",
                "description": "Python framework for building APIs",
                "difficulty": "Intermediate",
            },
            {
                "name": "Machine Learning",
                "description": "Methods for building systems that learn from data",
                "difficulty": "Advanced",
            },
        ]
    ])

    monkeypatch.setattr(
        "app.repositories.graph_repository.get_driver",
        lambda: fake_driver,
    )

    repository = GraphRepository()

    result = repository.get_related_skills(
        "Python"
    )

    assert len(result) == 2
    assert result[0]["name"] == "FastAPI"
    assert result[1]["name"] == "Machine Learning"


def test_get_career_paths(monkeypatch):

    fake_driver = FakeDriver([
        [
            {
                "job": "ML Engineer",
                "path": [
                    "Python",
                    "Machine Learning",
                    "ML Engineer",
                ],
                "distance": 2,
            },
            {
                "job": "Backend Developer",
                "path": [
                    "Python",
                    "FastAPI",
                    "Backend Developer",
                ],
                "distance": 2,
            },
        ]
    ])

    monkeypatch.setattr(
        "app.repositories.graph_repository.get_driver",
        lambda: fake_driver,
    )

    repository = GraphRepository()

    result = repository.get_career_paths(
        "Python"
    )

    assert len(result) == 2

    assert result[0]["job"] == "ML Engineer"
    assert result[0]["distance"] == 2

    assert result[1]["job"] == "Backend Developer"


def test_get_recommendations(monkeypatch):

    fake_driver = FakeDriver([
        [
            {
                "skill": "FastAPI",
                "difficulty": "Intermediate",
                "description": "Python framework for building APIs",
                "careers": [
                    "Backend Developer",
                    "Full Stack Developer",
                ],
            }
        ]
    ])

    monkeypatch.setattr(
        "app.repositories.graph_repository.get_driver",
        lambda: fake_driver,
    )

    repository = GraphRepository()

    result = repository.get_recommendations(
        "Python"
    )

    assert len(result) == 1

    assert result[0]["skill"] == "FastAPI"

    assert "Backend Developer" in (
        result[0]["careers"]
    )


def test_get_learning_path(monkeypatch):

    fake_driver = FakeDriver([
        [
            {
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
        ]
    ])

    monkeypatch.setattr(
        "app.repositories.graph_repository.get_driver",
        lambda: fake_driver,
    )

    repository = GraphRepository()

    result = repository.get_learning_path(
        "Python",
        "ML Engineer",
    )

    assert result is not None

    assert result["skill"] == "Python"
    assert result["job"] == "ML Engineer"
    assert result["distance"] == 2

    assert result["path"][0]["name"] == "Python"

    assert (
        result["path"][1]["name"]
        == "Machine Learning"
    )

    assert (
        result["path"][2]["name"]
        == "ML Engineer"
    )