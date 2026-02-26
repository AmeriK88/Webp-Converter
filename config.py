import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change_me")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "instance" / "uploads"))
    STATIC_FOLDER = str(BASE_DIR / "app" / "static")
    TEMPLATE_FOLDER = str(BASE_DIR / "app" / "templates")
    ALLOWED_EXTENSIONS = frozenset({"png", "jpg", "jpeg", "gif", "bmp"})
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
