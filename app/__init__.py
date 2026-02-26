"""
Application factory for the webP converter Flask app.
"""
from flask import Flask
from config import Config


def create_app(config_class=Config):
    """
    Create and configure the Flask application.
    
    Args:
        config_class: Configuration class to use (default: Config)
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(
        __name__,
        static_folder=config_class.STATIC_FOLDER,
        template_folder=config_class.TEMPLATE_FOLDER,
    )
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Ensure upload folder exists
    import os
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    # Register blueprints
    from app.web import web_bp
    app.register_blueprint(web_bp)
    
    return app
