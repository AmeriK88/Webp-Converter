"""
Image conversion service.
Handles WebP conversion and related operations.
"""
from PIL import Image
import os
from pathlib import Path
from typing import Tuple, List
from app.utils.files import allowed_file, get_safe_filename


class ImageService:
    """Service for handling image conversions."""
    
    def __init__(self, upload_folder: str, allowed_extensions: set):
        """
        Initialize the ImageService.
        
        Args:
            upload_folder: Path to the uploads folder
            allowed_extensions: Set of allowed file extensions
        """
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
    
    def is_valid_file(self, filename: str) -> bool:
        """
        Check if a file is valid for conversion.
        
        Args:
            filename: The filename to validate
            
        Returns:
            True if valid, False otherwise
        """
        return allowed_file(filename, self.allowed_extensions)
    
    def convert_to_webp(
        self,
        input_file,
        output_filename: str,
    ) -> Tuple[bool, str]:
        """
        Convert an image to WebP format.
        
        Args:
            input_file: File object to convert
            output_filename: Name for the output file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            output_path = os.path.join(self.upload_folder, output_filename)
            
            # Open and save as WebP
            img = Image.open(input_file)
            img.save(output_path, "WEBP")
            
            return True, f"Successfully converted to {output_filename}"
        
        except Exception as exc:
            return False, f"Error converting image: {str(exc)}"
    
    def ensure_upload_folder_exists(self) -> None:
        """Ensure the upload folder exists."""
        os.makedirs(self.upload_folder, exist_ok=True)
