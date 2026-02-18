from flask import Blueprint, request, send_file
import io

from stego.image.lsb import embed_lsb, extract_lsb
from stego.image.lsb_keyed import embed_lsb_keyed, extract_lsb_keyed
from stego.image.normalize import normalize_image

from utils.validators import validate_secret, validate_image_file
from utils.response import success, error

# 🔥 IMPORTANT: add /api prefix to match frontend
stego_bp = Blueprint("stego", __name__, url_prefix="/api/stego")


# ======================================================
# IMAGE STEGANOGRAPHY - EMBED
# ======================================================

@stego_bp.route("/image/embed", methods=["POST"])
def embed_image():
    try:
        # -------- Validate file --------
        if "file" not in request.files:
            return error("Cover image required", 400)

        file = request.files["file"]
        validate_image_file(file)

        # -------- Validate form data --------
        secret = request.form.get("secret")
        algorithm = request.form.get("algorithm", "lsb").lower()
        password = request.form.get("password", "")

        validate_secret(secret)

        # -------- Normalize image --------
        image = normalize_image(file)

        # -------- Algorithm selection --------
        if algorithm == "lsb":
            stego_image = embed_lsb(image, secret)

        elif algorithm == "lsb-keyed":
            if not password:
                return error("Password required for AES-keyed LSB", 400)

            stego_image = embed_lsb_keyed(image, secret, password)

        else:
            return error("Invalid algorithm", 400)

        # -------- Return PNG output --------
        buffer = io.BytesIO()
        stego_image.save(buffer, format="PNG")
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="image/png",
            as_attachment=True,
            download_name="deeptrace_stego.png"
        )

    except ValueError as ve:
        return error(str(ve), 400)

    except Exception as e:
        print("Embed Error:", e)
        return error("Internal server error", 500)


# ======================================================
# IMAGE STEGANOGRAPHY - EXTRACT
# ======================================================

@stego_bp.route("/image/extract", methods=["POST"])
def extract_image():
    try:
        # -------- Validate file --------
        if "file" not in request.files:
            return error("Stego image required", 400)

        file = request.files["file"]
        validate_image_file(file)

        # -------- Get form data --------
        algorithm = request.form.get("algorithm", "lsb").lower()
        password = request.form.get("password", "")

        # -------- Normalize image --------
        image = normalize_image(file)

        # -------- Algorithm selection --------
        if algorithm == "lsb":
            message = extract_lsb(image)

        elif algorithm == "lsb-keyed":
            if not password:
                return error("Password required for AES-keyed extraction", 400)

            message = extract_lsb_keyed(image, password)

        else:
            return error("Invalid algorithm", 400)

        if not message:
            return error("No hidden message detected", 400)

        return success(
            "Message extracted successfully",
            {"message": message}
        )

    except ValueError as ve:
        return error(str(ve), 400)

    except Exception as e:
        print("Extract Error:", e)
        return error("Internal server error", 500)