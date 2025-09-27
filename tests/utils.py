import contextlib

from git import Repo


@contextlib.contextmanager
def with_empty_commit(repo: Repo):
    repo.git.execute(["git", "commit", "--allow-empty", "-m", "dirty commit"])
    try:
        yield
    finally:
        repo.git.execute(["git", "reset", "--soft", "HEAD~1"])
