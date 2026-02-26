"""Web blueprint for the webP converter application."""
from flask import Blueprint

web_bp = Blueprint("web", __name__)

from . import routes  # noqa: E402, F401
