from app.repositories.graph_repository import GraphRepository


class JobService:

    def __init__(self):
        self.repository = GraphRepository()

    def get_all_jobs(self):
        return self.repository.get_all_jobs()

    def get_job(self, job_title: str):
        return self.repository.get_job(job_title)