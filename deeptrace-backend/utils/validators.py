ALLOWED_IMAGE_EXTENSIONS = {
    "png", "jpg", "jpeg", "bmp", "tiff", "webp", "gif", "heic", "heif"
}


def is_allowed_image(filename):
    """
    Validate allowed image extensions
    """
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )


def validate_secret(secret):
    """
    Validate secret message
    - Can be stripped safely
    """
    if secret is None or not str(secret).strip():
        raise ValueError("Secret message cannot be empty")


def validate_cover_text(text):
    """
    Validate cover / stego text
    IMPORTANT:
    - DO NOT strip
    - DO NOT normalize
    - Preserve whitespace & zero-width chars
    """
    if text is None:
        raise ValueError("Cover text is required")

    if not isinstance(text, str):
        raise ValueError("Cover text must be a string")

    if len(text) < 2:
        raise ValueError("Cover text is too short for steganography")


def validate_stego_text(text):
    """
    Validate stego text before extraction
    Same rules as cover text
    """
    if text is None:
        raise ValueError("Stego text is required")

    if not isinstance(text, str):
        raise ValueError("Stego text must be a string")

    if len(text) < 2:
        raise ValueError("Stego text is too short or invalid")