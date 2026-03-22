from pathlib import Path

from dunamai import Pattern, _detect_vcs, _detect_vcs_from_archival
from dunamai import Version as _Version


# FIXME: remove this monkey patch after new version of dunamai is released with the patch
class Version(_Version):
    @classmethod
    def from_any_vcs(
        cls,
        pattern: str | Pattern = Pattern.Default,
        latest_tag: bool = False,
        tag_dir: str = "tags",
        tag_branch: str | None = None,
        full_commit: bool = False,
        strict: bool = False,
        path: Path | None = None,
        pattern_prefix: str | None = None,
        ignore_untracked: bool = False,
        commit_length: int | None = None,
        highest_tag: bool = False,
    ):
        vcs = _detect_vcs_from_archival(path)
        if vcs is None:
            vcs = _detect_vcs(None, path)
        return cls._do_vcs_callback(
            vcs,
            pattern,
            latest_tag,
            tag_dir,
            tag_branch,
            full_commit,
            strict,
            path,
            pattern_prefix,
            ignore_untracked,
            commit_length,
            highest_tag,
        )
