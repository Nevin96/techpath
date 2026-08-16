from neo4j import GraphDatabase

from app.config import (
    COGNODB_URI,
    COGNODB_USERNAME,
    COGNODB_PASSWORD,
    COGNODB_DATABASE,
)


driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USERNAME, COGNODB_PASSWORD),
)


def create_constraints(tx):
    queries = [
        """
        CREATE CONSTRAINT skill_name_unique IF NOT EXISTS
        FOR (s:Skill)
        REQUIRE s.name IS UNIQUE
        """,
        """
        CREATE CONSTRAINT job_title_unique IF NOT EXISTS
        FOR (j:Job)
        REQUIRE j.title IS UNIQUE
        """,
        """
        CREATE CONSTRAINT technology_name_unique IF NOT EXISTS
        FOR (t:Technology)
        REQUIRE t.name IS UNIQUE
        """,
        """
        CREATE CONSTRAINT category_name_unique IF NOT EXISTS
        FOR (c:Category)
        REQUIRE c.name IS UNIQUE
        """,
    ]

    for query in queries:
        tx.run(query)


def create_categories(tx):
    categories = [
        "Programming",
        "Backend",
        "Frontend",
        "Data Science",
        "AI/ML",
        "DevOps",
        "Cloud",
    ]

    query = """
    UNWIND $categories AS category_name
    MERGE (c:Category {name: category_name})
    """

    tx.run(query, categories=categories)


def create_skills(tx):
    skills = [
        {
            "name": "Python",
            "description": "General-purpose programming language",
            "difficulty": "Beginner",
        },
        {
            "name": "Java",
            "description": "Object-oriented programming language",
            "difficulty": "Intermediate",
        },
        {
            "name": "JavaScript",
            "description": "Programming language for web applications",
            "difficulty": "Beginner",
        },
        {
            "name": "SQL",
            "description": "Language for querying relational databases",
            "difficulty": "Beginner",
        },
        {
            "name": "Git",
            "description": "Distributed version control system",
            "difficulty": "Beginner",
        },
        {
            "name": "Linux",
            "description": "Operating system and command-line environment",
            "difficulty": "Intermediate",
        },
        {
            "name": "Docker",
            "description": "Containerization platform",
            "difficulty": "Intermediate",
        },
        {
            "name": "Kubernetes",
            "description": "Container orchestration platform",
            "difficulty": "Advanced",
        },
        {
            "name": "React",
            "description": "JavaScript library for building user interfaces",
            "difficulty": "Intermediate",
        },
        {
            "name": "FastAPI",
            "description": "Python framework for building APIs",
            "difficulty": "Intermediate",
        },
        {
            "name": "Spring Boot",
            "description": "Java framework for backend applications",
            "difficulty": "Intermediate",
        },
        {
            "name": "NumPy",
            "description": "Python library for numerical computing",
            "difficulty": "Intermediate",
        },
        {
            "name": "Pandas",
            "description": "Python library for data analysis",
            "difficulty": "Intermediate",
        },
        {
            "name": "Statistics",
            "description": "Mathematical methods for analyzing data",
            "difficulty": "Intermediate",
        },
        {
            "name": "Machine Learning",
            "description": "Methods for building systems that learn from data",
            "difficulty": "Advanced",
        },
        {
            "name": "Deep Learning",
            "description": "Machine learning using multi-layer neural networks",
            "difficulty": "Advanced",
        },
        {
            "name": "PyTorch",
            "description": "Deep learning framework",
            "difficulty": "Advanced",
        },
        {
            "name": "TensorFlow",
            "description": "Machine learning framework",
            "difficulty": "Advanced",
        },
        {
            "name": "Redis",
            "description": "In-memory data store",
            "difficulty": "Intermediate",
        },
        {
            "name": "Kafka",
            "description": "Distributed event streaming platform",
            "difficulty": "Advanced",
        },
        {
            "name": "Cloud Computing",
            "description": "Using cloud platforms and infrastructure to build and deploy applications",
            "difficulty": "Intermediate",
        },
        {
            "name": "AWS",
            "description": "Amazon Web Services cloud platform",
            "difficulty": "Intermediate",
        },
    ]

    query = """
    UNWIND $skills AS skill
    MERGE (s:Skill {name: skill.name})
    SET s.description = skill.description,
        s.difficulty = skill.difficulty
    """

    tx.run(query, skills=skills)


def create_jobs(tx):
    jobs = [
        {
            "title": "Backend Developer",
            "description": "Build and maintain backend services and APIs",
        },
        {
            "title": "Frontend Developer",
            "description": "Build web interfaces and frontend applications",
        },
        {
            "title": "Full Stack Developer",
            "description": "Build both frontend and backend applications",
        },
        {
            "title": "Data Scientist",
            "description": "Analyze data and build predictive models",
        },
        {
            "title": "ML Engineer",
            "description": "Build and deploy machine learning systems",
        },
        {
            "title": "AI Engineer",
            "description": "Develop artificial intelligence applications",
        },
        {
            "title": "DevOps Engineer",
            "description": "Build and maintain deployment infrastructure",
        },
        {
            "title": "Cloud Engineer",
            "description": "Design and manage cloud infrastructure",
        },
        {
            "title": "Java Developer",
            "description": "Develop applications using Java technologies",
        },
        {
            "title": "Python Developer",
            "description": "Develop applications using Python technologies",
        },
    ]

    query = """
    UNWIND $jobs AS job
    MERGE (j:Job {title: job.title})
    SET j.description = job.description
    """

    tx.run(query, jobs=jobs)


def create_technologies(tx):
    technologies = [
        {"name": "FastAPI", "category": "Backend"},
        {"name": "Django", "category": "Backend"},
        {"name": "React", "category": "Frontend"},
        {"name": "Spring Boot", "category": "Backend"},
        {"name": "Docker", "category": "DevOps"},
        {"name": "Kubernetes", "category": "DevOps"},
        {"name": "PyTorch", "category": "AI/ML"},
        {"name": "TensorFlow", "category": "AI/ML"},
        {"name": "AWS", "category": "Cloud"},
        {"name": "Kafka", "category": "Backend"},
        {"name": "Redis", "category": "Backend"},
    ]

    query = """
    UNWIND $technologies AS technology
    MERGE (t:Technology {name: technology.name})
    SET t.category = technology.category
    """

    tx.run(query, technologies=technologies)


def create_category_relationships(tx):
    relationships = [
        ("Python", "Programming"),
        ("Java", "Programming"),
        ("JavaScript", "Programming"),
        ("SQL", "Programming"),
        ("Git", "Programming"),
        ("Linux", "DevOps"),
        ("Docker", "DevOps"),
        ("Kubernetes", "DevOps"),
        ("React", "Frontend"),
        ("FastAPI", "Backend"),
        ("Spring Boot", "Backend"),
        ("NumPy", "Data Science"),
        ("Pandas", "Data Science"),
        ("Statistics", "Data Science"),
        ("Machine Learning", "AI/ML"),
        ("Deep Learning", "AI/ML"),
        ("PyTorch", "AI/ML"),
        ("TensorFlow", "AI/ML"),
        ("Redis", "Backend"),
        ("Kafka", "Backend"),
        ("Cloud Computing", "Cloud"),
        ("AWS", "Cloud"),
        ("Cloud Computing", "AWS"),
        ("Linux", "Cloud Computing"),
        ("Docker", "Cloud Computing"),
    ]

    query = """
    UNWIND $relationships AS rel
    MATCH (s:Skill {name: rel.skill})
    MATCH (c:Category {name: rel.category})
    MERGE (s)-[:BELONGS_TO]->(c)
    """

    data = [
        {"skill": skill, "category": category}
        for skill, category in relationships
    ]

    tx.run(query, relationships=data)


def create_prerequisite_relationships(tx):
    relationships = [
        ("Python", "NumPy"),
        ("NumPy", "Pandas"),
        ("Python", "FastAPI"),
        ("Java", "Spring Boot"),
        ("JavaScript", "React"),
        ("Linux", "Docker"),
        ("Docker", "Kubernetes"),
        ("Python", "Machine Learning"),
        ("Statistics", "Machine Learning"),
        ("Pandas", "Machine Learning"),
        ("Machine Learning", "Deep Learning"),
        ("Deep Learning", "PyTorch"),
        ("Deep Learning", "TensorFlow"),
    ]

    query = """
    UNWIND $relationships AS rel
    MATCH (a:Skill {name: rel.from})
    MATCH (b:Skill {name: rel.to})
    MERGE (a)-[:PREREQUISITE_OF]->(b)
    """

    data = [
        {"from": source, "to": target}
        for source, target in relationships
    ]

    tx.run(query, relationships=data)


def create_related_relationships(tx):
    relationships = [
        ("Python", "SQL"),
        ("Python", "Statistics"),
        ("Python", "Machine Learning"),
        ("Java", "Spring Boot"),
        ("JavaScript", "React"),
        ("Docker", "Kubernetes"),
        ("Machine Learning", "Deep Learning"),
        ("Pandas", "Machine Learning"),
        ("PyTorch", "Deep Learning"),
        ("TensorFlow", "Deep Learning")
    ]

    query = """
    UNWIND $relationships AS rel
    MATCH (a:Skill {name: rel.from})
    MATCH (b:Skill {name: rel.to})
    MERGE (a)-[:RELATED_TO]->(b)
    """

    data = [
        {"from": source, "to": target}
        for source, target in relationships
    ]

    tx.run(query, relationships=data)


def create_job_relationships(tx):
    relationships = [
    ("Python", "Python Developer"),
    ("Java", "Java Developer"),
    ("Java", "Backend Developer"),

    ("JavaScript", "Frontend Developer"),
    ("React", "Frontend Developer"),

    ("FastAPI", "Backend Developer"),

    ("Pandas", "Data Scientist"),
    ("Statistics", "Data Scientist"),

    ("Machine Learning", "ML Engineer"),
    ("PyTorch", "ML Engineer"),

    ("Machine Learning", "AI Engineer"),
    ("Deep Learning", "AI Engineer"),

    ("React", "Full Stack Developer"),
    ("FastAPI", "Full Stack Developer"),
]

    query = """
    UNWIND $relationships AS rel
    MATCH (s:Skill {name: rel.skill})
    MATCH (j:Job {title: rel.job})
    MERGE (s)-[:REQUIRED_FOR]->(j)
    """

    data = [
        {"skill": skill, "job": job}
        for skill, job in relationships
    ]

    tx.run(query, relationships=data)


def create_technology_relationships(tx):
    relationships = [
        ("FastAPI", "Backend Developer"),
        ("Django", "Python Developer"),
        ("React", "Frontend Developer"),
        ("Spring Boot", "Java Developer"),
        ("Docker", "DevOps Engineer"),
        ("Kubernetes", "DevOps Engineer"),
        ("Docker", "Cloud Engineer"),
        ("Kubernetes", "Cloud Engineer"),
        ("PyTorch", "ML Engineer"),
        ("TensorFlow", "AI Engineer"),
        ("AWS", "Cloud Engineer"),
        ("Kafka", "Backend Developer"),
        ("Redis", "Backend Developer"),
    ]

    query = """
    UNWIND $relationships AS rel
    MATCH (t:Technology {name: rel.technology})
    MATCH (j:Job {title: rel.job})
    MERGE (t)-[:USED_BY]->(j)
    """

    data = [
        {"technology": technology, "job": job}
        for technology, job in relationships
    ]

    tx.run(query, relationships=data)


def seed_database():
    with driver.session(database=COGNODB_DATABASE) as session:
        session.execute_write(create_constraints)
        session.execute_write(create_categories)
        session.execute_write(create_skills)
        session.execute_write(create_jobs)
        session.execute_write(create_technologies)
        session.execute_write(create_category_relationships)
        session.execute_write(create_prerequisite_relationships)
        session.execute_write(create_related_relationships)
        session.execute_write(create_job_relationships)
        session.execute_write(create_technology_relationships)

    print("Database seeded successfully.")


if __name__ == "__main__":
    try:
        driver.verify_connectivity()
        print("Connected to CognoDB.")

        seed_database()

    finally:
        driver.close()