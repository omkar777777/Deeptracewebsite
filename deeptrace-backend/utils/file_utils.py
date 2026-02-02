import os
import uuid

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"


def ensure_dirs():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_uploaded_file(file):
    """
    Saves uploaded file with a unique name
    """
    ensure_dirs()
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    file.save(path)
    return path


def generate_output_path(extension="png"):
    """
    Generates unique output file path
    """
    ensure_dirs()
    filename = f"stego_{uuid.uuid4().hex}.{extension}"
    return os.path.join(OUTPUT_DIR, filename)