"""
Utility functions for file handling and validation.
"""

from __future__ import annotations

from typing import Set, Optional
from uuid import uuid4
from werkzeug.utils import secure_filename


def get_extension(filename: str) -> str:
    """
    Return the lowercase file extension without the dot.
    If no extension is present, returns an empty string.
    """
    if not filename or "." not in filename:
        return ""
    return filename.rsplit(".", 1)[1].strip().lower()


def allowed_file(filename: str, allowed_extensions: Set[str]) -> bool:
    """
    Check if a file has an allowed extension.

    Args:
        filename: The filename to check
        allowed_extensions: Set of allowed file extensions (without dots)

    Returns:
        True if the file is allowed, False otherwise
    """
    ext = get_extension(filename)
    return bool(ext) and ext in allowed_extensions


def get_safe_filename(filename: str, fallback: str = "file") -> str:
    """
    Get a secure filename using werkzeug. If the result is empty,
    returns a safe fallback.

    Args:
        filename: The original filename
        fallback: Used if secure_filename returns an empty string

    Returns:
        A secure filename
    """
    safe = secure_filename(filename or "")
    return safe if safe else fallback


def unique_filename(base: str, ext: str, max_base_len: int = 50) -> str:
    """
    Build a unique filename like: <base>_<8chars>.<ext>

    Args:
        base: Base name (will be secured)
        ext: Extension without dot (e.g. 'webp')
        max_base_len: Truncate base to keep filenames short

    Returns:
        Unique secure filename
    """
    base_safe = get_safe_filename(base, fallback="file")
    base_safe = base_safe.rsplit(".", 1)[0]  # por si te pasan "algo.webp"
    base_safe = base_safe[:max_base_len].rstrip("_-")

    token = uuid4().hex[:8]
    ext = (ext or "").strip().lower().lstrip(".") or "bin"

    return f"{base_safe}_{token}.{ext}"