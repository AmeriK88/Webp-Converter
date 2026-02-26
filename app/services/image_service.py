"""
Image conversion service.
Handles WebP conversion and related operations.
"""

import os
import io
from typing import Tuple, Optional
from PIL import Image, ImageCms, UnidentifiedImageError
from app.utils.files import allowed_file


class ImageService:
    """Service for handling image conversions."""

    def __init__(self, upload_folder: str, allowed_extensions: set, quality: int = 80):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions
        self.quality = quality

    def is_valid_file(self, filename: str) -> bool:
        return allowed_file(filename, self.allowed_extensions)

    def _to_srgb_if_profiled(
        self, img: Image.Image
    ) -> Tuple[Image.Image, Optional[bytes]]:
        """
        If image has an ICC profile, convert to sRGB for consistent browser rendering.
        Returns (converted_img, icc_profile_to_embed).

        Note: Pillow typing declares ImageCms.profileToProfile may return None,
        so we handle that explicitly for type-safety.
        """
        icc_profile: Optional[bytes] = img.info.get("icc_profile")
        if not icc_profile:
            return img, None

        try:
            src_profile = ImageCms.ImageCmsProfile(io.BytesIO(icc_profile))
            dst_profile = ImageCms.createProfile("sRGB")

            out_mode = "RGBA" if "A" in img.getbands() else "RGB"

            converted = ImageCms.profileToProfile(
                img,
                src_profile,
                dst_profile,
                outputMode=out_mode,
            )

            # Pillow types say this can be None, so fallback safely
            if converted is None:
                return img, icc_profile

            # Try embedding sRGB ICC profile bytes (may fail depending on Pillow build)
            srgb_icc: Optional[bytes]
            try:
                srgb_icc = ImageCms.ImageCmsProfile(dst_profile).tobytes()
            except Exception:
                srgb_icc = None

            return converted, srgb_icc

        except Exception:
            # If conversion fails, keep original pixels but embed original ICC
            return img, icc_profile

    def convert_to_webp(self, input_file, output_filename: str) -> Tuple[bool, str]:
        output_path = os.path.join(self.upload_folder, output_filename)

        try:
            input_file.stream.seek(0)

            # Validate real image
            with Image.open(input_file.stream) as img:
                img.verify()

            input_file.stream.seek(0)
            with Image.open(input_file.stream) as img:
                # Convert color profile to sRGB if needed
                img, icc_to_embed = self._to_srgb_if_profiled(img)

                # Ensure mode compatible with WebP
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA" if "A" in img.getbands() else "RGB")

                save_kwargs = {
                    "quality": self.quality,
                    "method": 6,
                    "optimize": True,
                }
                if icc_to_embed:
                    save_kwargs["icc_profile"] = icc_to_embed

                img.save(output_path, "WEBP", **save_kwargs)

            return True, f"Successfully converted to {output_filename}"

        except UnidentifiedImageError:
            return False, "File is not a valid image."

        except Exception as exc:
            return False, f"Conversion failed: {str(exc)}"

    def ensure_upload_folder_exists(self) -> None:
        os.makedirs(self.upload_folder, exist_ok=True)