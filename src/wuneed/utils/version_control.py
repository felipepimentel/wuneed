import git
import os

class VersionControl:
    def __init__(self):
        self.repo = None
        self.initialize_repo()

    def initialize_repo(self):
        try:
            self.repo = git.Repo(os.getcwd(), search_parent_directories=True)
        except git.exc.InvalidGitRepositoryError:
            print("Not a git repository. Some features may be limited.")

    def get_current_branch(self):
        if self.repo:
            return self.repo.active_branch.name
        return None

    def get_last_commit(self):
        if self.repo:
            return self.repo.head.commit.hexsha
        return None

    def get_modified_files(self):
        if self.repo:
            return [item.a_path for item in self.repo.index.diff(None)]
        return []

version_control = VersionControl()