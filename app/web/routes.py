"""
Web routes for the webP converter application.
Handles file uploads, downloads, and conversions.
"""
from flask import render_template, request, redirect, url_for, flash, send_from_directory, current_app
from datetime import datetime
from . import web_bp
from app.services.image_service import ImageService
from app.utils.files import get_safe_filename


@web_bp.route("/")
def index():
    """Landing page with cache-buster timestamp for static files."""
    return render_template("index.html", ts=datetime.utcnow().timestamp())


@web_bp.route("/download/<filename>")
def download_image(filename):
    """Download a converted image."""
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@web_bp.route("/uploads/<filename>")
def uploaded_file(filename):
    """Serve an uploaded/converted file."""
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@web_bp.route("/convert", methods=["POST"])
def convert():
    """Convert uploaded images to WebP format."""
    # Initialize service
    image_service = ImageService(
        current_app.config["UPLOAD_FOLDER"],
        current_app.config["ALLOWED_EXTENSIONS"]
    )
    image_service.ensure_upload_folder_exists()
    
    # Get form data
    input_images = request.files.getlist("input_images")
    output_prefix = request.form.get("output_prefix", "image")
    
    if not input_images:
        flash("No files selected", "error")
        return redirect(url_for("web.index"))
    
    converted_urls = []
    idx = 0
    
    for in_img in input_images:
        if in_img.filename == "":
            continue
        
        # Validate file
        if not image_service.is_valid_file(in_img.filename):
            flash(f"Invalid file type: {in_img.filename}", "error")
            return redirect(url_for("web.index"))
        
        # Generate safe output filename
        out_name = f"{output_prefix}_{idx}.webp"
        
        # Convert image
        success, message = image_service.convert_to_webp(in_img, out_name)
        
        if success:
            converted_urls.append(url_for("web.uploaded_file", filename=out_name))
            idx += 1
        else:
            flash(f"Error converting {in_img.filename}: {message}", "error")
            return redirect(url_for("web.index"))
    
    # Flash results
    if converted_urls:
        flash("|".join(converted_urls), "converted")
        flash(f"{idx} image(s) successfully converted", "success")
    
    return redirect(url_for("web.index"))
