from contextlib import contextmanager


@contextmanager
def safe_checkout(ref, repo):
    git = repo.git
    was_dirty = False
    if repo.is_dirty():
        git.stash("save", "include-untracked")
        was_dirty = True
    current_branch = repo.head.ref.name

    print(f"Checking out {ref}")
    git.checkout(ref)

    try:
        yield

    finally:
        git.checkout(current_branch)
        if was_dirty:
            git.stash("pop")
