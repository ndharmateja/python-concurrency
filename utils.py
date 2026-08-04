import time
from pathlib import Path
import shutil

def print_duration(start, finish):
    ms = (finish - start) / 1_000_000
    if ms > 10000:
        print(f"finished in {round(ms / 1000, 2)} s")
    else:
        print(f"finished in {round(ms, 2)} ms")

def fn(seconds=1):
    print(f"Sleeping {seconds} sec")
    time.sleep(seconds)
    print("Sleeping done")

def print_countdown(t):
    for i in range(t):
        print(f"{i}s")
        time.sleep(1)
    print(f"{t}s")

def create_folder_if_not_exists(folder_path: str | Path) -> None:
    """Creates a folder (and any missing parent directories) if it doesn't exist."""
    Path(folder_path).mkdir(parents=True, exist_ok=True)


def delete_folder_contents(folder_path: str | Path) -> None:
    """Deletes all files, subdirectories, and symlinks inside the specified folder."""
    folder = Path(folder_path)
    
    if not folder.exists() or not folder.is_dir():
        return

    for item in folder.iterdir():
        if item.is_file() or item.is_symlink():
            item.unlink()  # Delete file or symbolic link
        elif item.is_dir():
            shutil.rmtree(item)  # Delete directory and all its contents