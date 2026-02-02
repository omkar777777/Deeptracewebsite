from flask import Blueprint, request, send_file
import io

from stego.text.whitespace import embed_whitespace, extract_whitespace
from stego.text.zerowidth import embed_zerowidth, extract_zerowidth

from utils.validators import (
    validate_secret,
    validate_cover_text,
    validate_stego_text
)
from utils.response import success, error

stego_bp = Blueprint("stego", __name__, url_prefix="/stego")


# ================= TEXT (FILE-BASED) =================

@stego_bp.route("/text/embed", methods=["POST"])
def embed_text():
    try:
        # ✅ FORCE JSON (no is_json gate)
        data = request.get_json(force=True)

        cover_text = data.get("cover_text")
        secret = data.get("secret")
        algorithm = data.get("algorithm", "").lower()

        validate_cover_text(cover_text)
        validate_secret(secret)

        if algorithm == "whitespace":
            stego_text = embed_whitespace(cover_text, secret)
        elif algorithm == "zerowidth":
            stego_text = embed_zerowidth(cover_text, secret)
        else:
            return error("Invalid algorithm", 400)

        buffer = io.BytesIO(stego_text.encode("utf-8"))
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="text/plain; charset=utf-8",
            as_attachment=True,
            download_name="stego.txt"
        )

    except Exception as e:
        return error(str(e), 400)


@stego_bp.route("/text/extract", methods=["POST"])
def extract_text():
    try:
        if "file" not in request.files:
            return error("Stego text file required", 400)

        algorithm = request.form.get("algorithm", "").lower()
        stego_text = request.files["file"].read().decode("utf-8")

        validate_stego_text(stego_text)

        if algorithm == "whitespace":
            secret = extract_whitespace(stego_text)
        elif algorithm == "zerowidth":
            secret = extract_zerowidth(stego_text)
        else:
            return error("Invalid algorithm", 400)

        return success("Text extracted", {"message": secret})

    except Exception as e:
        return error(str(e), 400)