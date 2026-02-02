from PIL import Image
import pillow_heif

# Enable HEIC / HEIF support
pillow_heif.register_heif_opener()

def normalize_image(file):
    """
    Accepts any image format (PNG, JPEG, HEIC, WEBP, etc.)
    Returns a normalized RGB PIL Image
    """
    img = Image.open(file)
    img = img.convert("RGB")  # normalize channels
    return img