import os
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from steganalysis.image_pipeline import analyze_image
from steganalysis.file_pipeline import analyze_file


steganalysis_bp = Blueprint("steganalysis", __name__)

UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB limit

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "tiff", "webp"}


# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@steganalysis_bp.route("/analyze", methods=["POST"])
def analyze():

    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if not file or file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Secure filename
    filename = secure_filename(file.filename)

    # Ensure extension exists
    if "." not in filename:
        return jsonify({"error": "File must have a valid extension"}), 400

    extension = filename.rsplit(".", 1)[1].lower()

    # Generate unique filename
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_name)

    try:
        # Save file temporarily
        file.save(filepath)

        # File size protection
        if os.path.getsize(filepath) > MAX_FILE_SIZE:
            os.remove(filepath)
            return jsonify({"error": "File exceeds maximum allowed size (20MB)"}), 400

        # Route to correct analysis pipeline
        if extension in ALLOWED_IMAGE_EXTENSIONS:
            result = analyze_image(filepath)
        else:
            result = analyze_file(filepath)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "error": "Analysis failed",
            "details": str(e)
        }), 500

    finally:
        # Clean up uploaded file safely
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass