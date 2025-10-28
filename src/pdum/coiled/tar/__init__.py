"""Helper utilities for creating in-memory tar archives."""

import io
import tarfile
from pathlib import Path
from typing import Iterator, Optional, Tuple, Union

from ..fs import find_pyproject_root, iter_git_files


def create_in_memory_tarball(
    gzipped: bool = False,
) -> Tuple[tarfile.TarFile, io.BytesIO]:
    """Create an in-memory tarball backed by BytesIO.

    Args:
        gzipped: If True, create a gzipped tar archive. Defaults to False.

    Returns:
        A tuple of (tarfile.TarFile, io.BytesIO) where:
        - The TarFile can be used to add files to the archive
        - The BytesIO can be used to retrieve the archive bytes after closing the TarFile

    Example:
        >>> tar, buffer = create_in_memory_tarball(gzipped=True)
        >>> # Add files to the tar
        >>> tar.add(...)
        >>> tar.close()
        >>> # Get the bytes
        >>> tarball_bytes = buffer.getvalue()
    """
    buffer = io.BytesIO()
    mode = "w:gz" if gzipped else "w"
    tar = tarfile.open(fileobj=buffer, mode=mode)
    return tar, buffer


def add_paths_to_tar(
    tar: tarfile.TarFile,
    paths: Iterator[Path],
    root: Union[str, Path],
) -> None:
    """Add files from an iterator to a tar archive with paths relative to root.

    For each path in the iterator, this function adds it to the tar archive with
    an arcname (archive name) that is relative to the specified root directory.

    Args:
        tar: The TarFile object to add files to (must be open for writing)
        paths: An iterator of Path objects to add to the archive
        root: The root directory to use for relativizing paths. Each path will
              be made relative to this directory for the archive name.

    Raises:
        ValueError: If a path is not relative to the specified root directory

    Example:
        >>> from pdum.coiled.tar import create_in_memory_tarball, add_paths_to_tar
        >>> from pdum.coiled.fs import iter_git_files
        >>> from pathlib import Path
        >>>
        >>> # Create an in-memory tarball
        >>> tar, buffer = create_in_memory_tarball(gzipped=True)
        >>>
        >>> # Add all git-tracked files
        >>> root = Path("/path/to/repo")
        >>> add_paths_to_tar(tar, iter_git_files(root), root)
        >>>
        >>> tar.close()
        >>> tarball_bytes = buffer.getvalue()
    """
    root_path = Path(root).resolve()

    for path in paths:
        try:
            # Get the relative path with respect to root
            relative_path = path.relative_to(root_path)
            # Add to tar with the relative path as the arcname
            tar.add(path, arcname=str(relative_path))
        except ValueError as e:
            raise ValueError(
                f"Path {path} is not relative to root directory {root_path}"
            ) from e


def project_tarball(*,
    start_path: Optional[Union[str, Path]] = None,
    gzipped: bool = False,
) -> io.BytesIO:
    """Create a tarball of all git-tracked files in a Python project.

    This is a convenience function that:
    1. Finds the project root by locating pyproject.toml
    2. Creates an in-memory tarball (optionally gzipped)
    3. Adds all git-tracked files from the project root
    4. Returns the tarball as bytes

    Args:
        start_path: The starting directory for finding the project root.
                   Defaults to current working directory.
        gzipped: If True, create a gzipped tar archive. Defaults to False.

    Returns:
        The tarball as bytes, ready to be written to a file or sent over network.

    Raises:
        FileNotFoundError: If pyproject.toml cannot be found or git is not installed.
        subprocess.CalledProcessError: If git command fails.

    Example:
        >>> from pdum.coiled.tar import project_tarball
        >>>
        >>> # Create a gzipped tarball of the current project
        >>> tarball_bytes = project_tarball(gzipped=True)
        >>>
        >>> # Write to a file
        >>> with open("project.tar.gz", "wb") as f:
        ...     f.write(tarball_bytes)
        >>>
        >>> # Or start from a specific subdirectory
        >>> tarball_bytes = project_tarball("/path/to/subdir", gzipped=True)
    """
    # Find the project root
    project_root = find_pyproject_root(start_path)

    # Create in-memory tarball
    tar, buffer = create_in_memory_tarball(gzipped=gzipped)

    # Add all git-tracked files relative to project root
    add_paths_to_tar(tar, iter_git_files(project_root), project_root)

    # Close tar and return bytes
    tar.close()
    buffer.seek(0)
    return buffer


__all__ = ["create_in_memory_tarball", "add_paths_to_tar", "project_tarball"]
