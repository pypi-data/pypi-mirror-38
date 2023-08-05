from pathlib import Path


def delete_dir_rec(path: Path):
    """
    Delete a folder recursive.
    :param path: folder to deleted
    """
    if not path.exists():
        return
    for sub in path.iterdir():
        if sub.is_dir():
            delete_dir_rec(sub)
        else:
            sub.unlink()
    path.rmdir()
