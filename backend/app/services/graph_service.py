from app.repositories.graph_repository import GraphRepository


class GraphService:

    def __init__(self):
        self.repository = GraphRepository()

    def get_all_skills(self):
        return self.repository.get_all_skills()

    def get_skill(self, skill_name: str):
        return self.repository.get_skill(skill_name)

    def get_related_skills(self, skill_name: str):
        return self.repository.get_related_skills(skill_name)

    def get_jobs_for_skill(self, skill_name: str):
        return self.repository.get_jobs_for_skill(skill_name)

    def get_career_paths(self, skill_name: str):
        return self.repository.get_career_paths(skill_name)
    def get_graph(self, skill_name: str):
        return self.repository.get_graph(skill_name)
    def get_recommendations(self, skill_name: str):
        return self.repository.get_recommendations(skill_name)