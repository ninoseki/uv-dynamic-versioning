import contextlib
from pathlib import Path

from git import Repo


@contextlib.contextmanager
def empty_commit(repo: Repo):
    repo.git.execute(["git", "commit", "--allow-empty", "-m", "dirty commit"])
    try:
        yield
    finally:
        repo.git.execute(["git", "reset", "--soft", "HEAD~1"])


@contextlib.contextmanager
def dirty(repo: Repo):
    assert repo.working_dir

    path = Path(repo.working_dir) / "dirty-file"
    path.write_text("dirty")
    try:
        yield
    finally:
        path.unlink(missing_ok=True)
