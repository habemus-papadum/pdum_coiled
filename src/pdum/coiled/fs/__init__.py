"""File system utilities for iterating over files respecting git ignore rules."""

import subprocess
from pathlib import Path
from typing import Iterator, Optional, Union


def iter_git_files(root: Union[str, Path] = ".") -> Iterator[Path]:
    """Iterate over all files in a git repository, respecting .gitignore rules.

    This function uses git's native `ls-files` command to list files, which means
    it leverages git's own implementation for handling .gitignore patterns. This is
    the most canonical way to respect git ignore rules.

    Args:
        root: The root directory to search. Defaults to current directory.
              Must be within a git repository.

    Yields:
        Path objects for each file in the repository that isn't ignored.

    Raises:
        FileNotFoundError: If git is not installed.
        subprocess.CalledProcessError: If the directory is not a git repository
                                       or git command fails.

    Example:
        >>> from pdum.coiled.fs import iter_git_files
        >>> for file_path in iter_git_files("/path/to/repo"):
        ...     print(file_path)
    """
    root_path = Path(root).resolve()

    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=root_path,
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as e:
        raise FileNotFoundError(
            "git command not found. Please ensure git is installed and in your PATH."
        ) from e
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output,
            e.stderr,
        ) from e

    for line in result.stdout.splitlines():
        if line.strip():  # Skip empty lines
            path = root_path / line.strip()
            # Only yield files that actually exist on the filesystem
            # (skip files that are in git index but deleted from working directory)
            if path.exists():
                yield path


def find_pyproject_root(start_path: Optional[Union[str, Path]] = None) -> Path:
    """Find the project root by traversing up until finding pyproject.toml.

    Starts from the given path (or current working directory if not provided) and
    traverses up the directory hierarchy until it finds a directory containing
    pyproject.toml.

    Args:
        start_path: The starting directory for the search. Defaults to current
                   working directory if not provided.

    Returns:
        The directory containing pyproject.toml.

    Raises:
        FileNotFoundError: If pyproject.toml cannot be found in any parent directory.

    Example:
        >>> from pdum.coiled.fs import find_pyproject_root
        >>> root = find_pyproject_root()
        >>> print(f"Project root: {root}")
        >>>
        >>> # Or start from a specific path
        >>> root = find_pyproject_root("/path/to/some/subdir")
    """
    if start_path is None:
        current = Path.cwd()
    else:
        current = Path(start_path).resolve()

    # Traverse up the directory tree
    for directory in [current, *current.parents]:
        pyproject_path = directory / "pyproject.toml"
        if pyproject_path.exists():
            return directory

    raise FileNotFoundError(
        f"Could not find pyproject.toml in {current} or any of its parent directories"
    )


__all__ = ["iter_git_files", "find_pyproject_root"]
