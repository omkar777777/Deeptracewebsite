from PIL import Image
import pillow_heif
import io

# Enable HEIC / HEIF support
pillow_heif.register_heif_opener()


def normalize_image(file):
    """
    Accepts ANY image format.
    Converts to clean RGB PNG-ready image.
    Returns fresh RGB PIL Image.
    """

    img = Image.open(file)

    # Convert to RGB (removes alpha and weird modes)
    img = img.convert("RGB")

    # 🔥 Force re-encode into clean PNG buffer
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    clean_img = Image.open(buffer).convert("RGB")

    return clean_img