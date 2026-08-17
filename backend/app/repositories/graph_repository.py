from app.database.neo4j import get_driver
from app.config import COGNODB_DATABASE

class GraphRepository:

    def __init__(self):
        self.driver = get_driver()
        self.database = COGNODB_DATABASE

    def get_all_skills(self):
        query = """
        MATCH (s:Skill)
        RETURN
            s.name AS name,
            s.description AS description,
            s.difficulty AS difficulty
        ORDER BY s.name
        """

        with self.driver.session(database=COGNODB_DATABASE) as session:
            result = session.run(query)

            return [record.data() for record in result]

    def get_skill(self, skill_name: str):
        query = """
        MATCH (s:Skill)
        WHERE toLower(s.name) = toLower($skill_name)
        RETURN
            s.name AS name,
            s.description AS description,
            s.difficulty AS difficulty
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(
                query,
                skill_name=skill_name
            )

            record = result.single()

            if record is None:
                return None

            return record.data()

    def get_related_skills(self, skill_name: str):
        query = """
        MATCH (s:Skill)
        WHERE toLower(s.name) = toLower($skill_name)

        MATCH (s)-[:RELATED_TO|PREREQUISITE_OF]->(related:Skill)

        RETURN DISTINCT
            related.name AS name,
            related.description AS description,
            related.difficulty AS difficulty

        ORDER BY related.name
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(
                query,
                skill_name=skill_name
            )

            return [record.data() for record in result]
    def get_jobs_for_skill(self, skill_name: str):
        query = """
        MATCH (s:Skill)
        WHERE toLower(s.name) = toLower($skill_name)

        MATCH (s)-[:REQUIRED_FOR]->(j:Job)

        RETURN
            j.title AS title,
            j.description AS description

        ORDER BY j.title
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(
                query,
                skill_name=skill_name
            )

            return [record.data() for record in result]

    def get_career_paths(self, skill_name: str):
        query = """
        MATCH (start:Skill)
        WHERE toLower(start.name) = toLower($skill_name)

        MATCH path =
            (start)-[:PREREQUISITE_OF*0..4]->
            (skill:Skill)
            -[:REQUIRED_FOR]->
            (job:Job)

        WITH job, path
        ORDER BY length(path)

        WITH job, collect(path)[0] AS shortest_path

        RETURN
            job.title AS job,
            [node IN nodes(shortest_path) |
                CASE
                    WHEN node:Skill THEN node.name
                    WHEN node:Job THEN node.title
                END
            ] AS path,
            length(shortest_path) AS distance

        ORDER BY distance, job
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(
                query,
                skill_name=skill_name
            )

            return [record.data() for record in result]
    def get_all_jobs(self):
        query = """
        MATCH (j:Job)
        RETURN
            j.title AS title,
            j.description AS description
        ORDER BY j.title
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(query)

            return [record.data() for record in result]


    def get_job(self, job_title: str):
        query = """
        MATCH (j:Job)
        WHERE toLower(j.title) = toLower($job_title)
        RETURN
            j.title AS title,
            j.description AS description
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(
                query,
                job_title=job_title
            )

            record = result.single()

            if record is None:
                return None

            return record.data()
    def get_graph(self, skill_name: str):
        node_query = """
        MATCH (start:Skill)
        WHERE toLower(start.name) = toLower($skill_name)

        MATCH p =
            (start)-[:PREREQUISITE_OF*0..4]->(skill:Skill)
            -[:REQUIRED_FOR]->(job:Job)

        UNWIND nodes(p) AS n

        WITH DISTINCT n

        RETURN
            CASE
                WHEN n:Job THEN n.title
                ELSE n.name
            END AS id,

            CASE
                WHEN n:Job THEN "job"
                ELSE "skill"
            END AS type,

            n.description AS description,

            CASE
                WHEN n:Job THEN null
                ELSE n.difficulty
            END AS difficulty

        ORDER BY id
        """

        edge_query = """
            MATCH (start:Skill)
            WHERE toLower(start.name) = toLower($skill_name)

            MATCH p =
                (start)-[:PREREQUISITE_OF*0..4]->(skill:Skill)
                -[:REQUIRED_FOR]->(job:Job)

            UNWIND relationships(p) AS r

            WITH
                startNode(r) AS sourceNode,
                endNode(r) AS targetNode,
                type(r) AS relationship

            RETURN DISTINCT

                CASE
                    WHEN sourceNode:Job THEN sourceNode.title
                    ELSE sourceNode.name
                END AS source,

                CASE
                    WHEN targetNode:Job THEN targetNode.title
                    ELSE targetNode.name
                END AS target,

                relationship
            """

        with self.driver.session(
            database=self.database
        ) as session:

            node_result = session.run(
                node_query,
                skill_name=skill_name
            )

            nodes = [
                record.data()
                for record in node_result
            ]

            edge_result = session.run(
                edge_query,
                skill_name=skill_name
            )

            edges = [
                record.data()
                for record in edge_result
            ]

            return {
                "nodes": nodes,
                "edges": edges
            }
    def get_recommendations(self, skill_name: str):

        query = """
        MATCH (start:Skill)
        WHERE toLower(start.name) = toLower($skill_name)

        MATCH (start)-[:PREREQUISITE_OF]->(next:Skill)

        OPTIONAL MATCH (next)-[:REQUIRED_FOR]->(job:Job)

        WITH
            next,
            collect(DISTINCT job.title) AS careers

        RETURN
            next.name AS skill,
            next.difficulty AS difficulty,
            next.description AS description,
            careers

        ORDER BY next.name
        """

        with self.driver.session(
            database=self.database
        ) as session:

            result = session.run(
                query,
                skill_name=skill_name
            )

            return [
                record.data()
                for record in result
            ]
    def get_learning_path(self,skill_name: str,job_name: str):
        query = """
        MATCH (start:Skill)
        WHERE toLower(start.name) = toLower($skill_name)

        MATCH (job:Job)
        WHERE toLower(job.title) = toLower($job_name)

        MATCH p =
            shortestPath(
                (start)-[:PREREQUISITE_OF|REQUIRED_FOR*1..8]->(job)
            )

        RETURN
            [node IN nodes(p) |
                CASE
                    WHEN node:Job THEN node.title
                    ELSE node.name
                END
            ] AS path,

            length(p) AS distance
        """

        with self.driver.session(
            database=self.database
        ) as session:

            result = session.run(
                query,
                skill_name=skill_name,
                job_name=job_name
            )

            record = result.single()

            if record is None:
                return None

            return {
                "skill": skill_name,
                "job": job_name,
                "path": record["path"],
                "distance": record["distance"]
            }