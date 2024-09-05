from wuneed.utils.version_control import version_control
from wuneed.ai.copilot import ai_copilot

class ContextRecommender:
    def __init__(self):
        self.vc = version_control

    def get_project_context(self):
        context = {
            'branch': self.vc.get_current_branch(),
            'last_commit': self.vc.get_last_commit(),
            'modified_files': self.vc.get_modified_files()
        }
        return context

    def recommend_command(self):
        context = self.get_project_context()
        query = f"Given the current project context: {context}, suggest a useful command."
        return ai_copilot.suggest_command(query)

context_recommender = ContextRecommender()