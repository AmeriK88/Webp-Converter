"""
Entry point for the webP converter application.
"""
import os
from app import create_app
from config import config

# Get the configuration
config_name = os.getenv("FLASK_ENV", "development")
config_class = config.get(config_name, config["default"])

# Create and run the app
app = create_app(config_class)

if __name__ == "__main__":
    app.run(debug=config_class.DEBUG)
