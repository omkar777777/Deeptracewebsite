import os


# ======================================================
# ALLOWED IMAGE EXTENSIONS
# ======================================================

ALLOWED_IMAGE_EXTENSIONS = {
    "png", "jpg", "jpeg", "bmp",
    "tiff", "webp", "gif",
    "heic", "heif"
}


# ======================================================
# IMAGE VALIDATION
# ======================================================

def is_allowed_image(filename: str) -> bool:
    """
    Validate allowed image extensions.
    Case-insensitive.
    """

    if not filename or "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_IMAGE_EXTENSIONS


def validate_image_file(file):
    """
    Optional stronger validation for uploaded image file.
    """

    if file is None:
        raise ValueError("Image file is required")

    if not file.filename:
        raise ValueError("Invalid file name")

    if not is_allowed_image(file.filename):
        raise ValueError("Unsupported image format")


# ======================================================
# SECRET MESSAGE VALIDATION
# ======================================================

def validate_secret(secret: str):
    """
    Validate secret message.
    - Must not be empty
    - Must be string
    - Limit max length (basic safety)
    """

    if secret is None:
        raise ValueError("Secret message is required")

    if not isinstance(secret, str):
        raise ValueError("Secret message must be a string")

    if not secret.strip():
        raise ValueError("Secret message cannot be empty")

    # Optional: protect against extreme payload sizes
    if len(secret.encode("utf-8")) > 1_000_000:
        raise ValueError("Secret message too large")