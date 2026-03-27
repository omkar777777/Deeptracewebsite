from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import uuid
from werkzeug.utils import secure_filename

# ======================================================
# App initialization
# ======================================================
app = Flask(__name__)

# 🔥 DEV MODE CORS (Allow all origins)
CORS(app)

# ======================================================
# Cryptography imports
# ======================================================
from crypto.caesar import encrypt_caesar, decrypt_caesar
from crypto.aes import encrypt_aes, decrypt_aes
from crypto.des import encrypt_des, decrypt_des
from crypto.tripledes import encrypt_3des, decrypt_3des
from crypto.blowfish import encrypt_blowfish, decrypt_blowfish
from crypto.rc4 import encrypt_rc4, decrypt_rc4
from crypto.chacha20 import encrypt_chacha20, decrypt_chacha20
from crypto.rsa import generate_rsa_keys, encrypt_rsa, decrypt_rsa

# ======================================================
# Steganography routes
# ======================================================
from routes.stego_routes import stego_bp
app.register_blueprint(stego_bp)

from watermark.routes import watermark_bp
app.register_blueprint(watermark_bp)

# ======================================================
# Steganalysis imports
# ======================================================
from steganalysis.image_pipeline import analyze_image
from steganalysis.file_pipeline import analyze_file

# ======================================================
# CRYPTOGRAPHY API
# ======================================================
@app.route("/api/crypto", methods=["POST"])
def crypto_handler():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    algorithm = data.get("algorithm")
    action = data.get("action")
    text = data.get("text")
    key = data.get("key")

    if not algorithm or not action:
        return jsonify({"error": "Missing required fields"}), 400

    try:

        # =====================
        # Caesar Cipher
        # =====================
        if algorithm == "caesar":
            shift = int(key)

            if action == "encrypt":
                result = encrypt_caesar(text, shift)
            elif action == "decrypt":
                result = decrypt_caesar(text, shift)
            else:
                return jsonify({"error": "Invalid action"}), 400

        # =====================
        # AES
        # =====================
        elif algorithm == "aes":
            result = encrypt_aes(text, key) if action == "encrypt" else decrypt_aes(text, key)

        elif algorithm == "des":
            result = encrypt_des(text, key) if action == "encrypt" else decrypt_des(text, key)

        elif algorithm == "3des":
            result = encrypt_3des(text, key) if action == "encrypt" else decrypt_3des(text, key)

        elif algorithm == "blowfish":
            result = encrypt_blowfish(text, key) if action == "encrypt" else decrypt_blowfish(text, key)

        elif algorithm == "rc4":
            result = encrypt_rc4(text, key) if action == "encrypt" else decrypt_rc4(text, key)

        elif algorithm == "chacha20":
            result = encrypt_chacha20(text, key) if action == "encrypt" else decrypt_chacha20(text, key)

        elif algorithm == "rsa":
            if action == "generate":
                result = generate_rsa_keys()

            elif action == "encrypt":
                result = encrypt_rsa(text, key)

            elif action == "decrypt":
                result = decrypt_rsa(text, key)

            else:
                return jsonify({"error": "Invalid RSA action"}), 400

        else:
            return jsonify({"error": "Unsupported algorithm"}), 400

        return jsonify({
            "algorithm": algorithm,
            "action": action,
            "result": result
        })

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


# ======================================================
# STEGANALYSIS API
# STEGANALYSIS API
# ======================================================
@app.route("/api/steganalysis/analyze", methods=["POST"])
def steganalysis_handler():

    MAX_FILE_SIZE = 20 * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "tiff", "webp"}

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    if "." not in filename:
        return jsonify({"error": "File must have a valid extension"}), 400

    extension = filename.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}_{filename}"

    # Save temporarily
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, unique_name)

    try:
        file.save(file_path)

        if os.path.getsize(file_path) > MAX_FILE_SIZE:
            os.remove(file_path)
            return jsonify({"error": "File exceeds 20MB limit"}), 400

        if extension in ALLOWED_IMAGE_EXTENSIONS:
            result = analyze_image(file_path)
        else:
            result = analyze_file(file_path)

        return jsonify(result)

    except RuntimeError as e:
        # Handle missing OpenCV gracefully
        return jsonify({
            "error": "Service Unavailable", 
            "details": str(e),
            "info": "This feature requires heavy libraries (OpenCV) not supported on Vercel Serverless. Please deploy to a full VPS if required."
        }), 503

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# ======================================================
# APP ENTRY POINT
# ======================================================
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
