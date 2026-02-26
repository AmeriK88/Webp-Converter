"""
Image conversion service.
Handles WebP conversion and related operations.
"""

import os
from typing import Tuple
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

    def _to_srgb_if_profiled(self, img: Image.Image) -> tuple[Image.Image, bytes | None]:
        """
        If image has an ICC profile, convert to sRGB for consistent browser rendering.
        Returns (converted_img, icc_profile_to_embed).
        """
        icc_profile = img.info.get("icc_profile")
        if not icc_profile:
            return img, None

        try:
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc_profile))  # type: ignore
            dst = ImageCms.createProfile("sRGB")
            # outputMode must match target later; use RGB/RGBA depending on alpha
            out_mode = "RGBA" if "A" in img.getbands() else "RGB"

            converted = ImageCms.profileToProfile(
                img,
                src,
                dst,
                outputMode=out_mode,
            )

            # Embed sRGB profile so other apps keep it consistent too
            srgb_icc = ImageCms.ImageCmsProfile(dst).tobytes()  # may fail on some builds
            return converted, srgb_icc
        except Exception:
            # If conversion fails, at least embed original profile to reduce shifts
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
                # Convert color profile to sRGB if needed (best fix for "weird colors")
                # NOTE: requires io import; added below
                img, icc_to_embed = self._to_srgb_if_profiled(img)

                # Ensure mode compatible with WebP
                if img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGBA" if "A" in img.getbands() else "RGB")

                save_kwargs = dict(
                    quality=self.quality,
                    method=6,
                    optimize=True,
                )
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