"""
Utility functions for file handling and validation.
"""
from werkzeug.utils import secure_filename
from typing import Set


def allowed_file(filename: str, allowed_extensions: Set[str]) -> bool:
    """
    Check if a file has an allowed extension.
    
    Args:
        filename: The filename to check
        allowed_extensions: Set of allowed file extensions (without dots)
        
    Returns:
        True if the file is allowed, False otherwise
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def get_safe_filename(filename: str) -> str:
    """
    Get a secure filename using werkzeug.
    
    Args:
        filename: The original filename
        
    Returns:
        A secure filename
    """
    return secure_filename(filename)
