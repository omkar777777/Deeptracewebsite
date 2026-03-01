from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile

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

# ======================================================
# Steganalysis imports
# ======================================================
from steganalysis.image_pipeline import analyze_image
from steganalysis.file_pipeline import analyze_file


# ======================================================
# App initialization
# ======================================================
app = Flask(__name__)
CORS(app)

# Register Blueprints
app.register_blueprint(stego_bp)
from watermark.routes import watermark_bp
app.register_blueprint(watermark_bp)


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
            if key is None:
                return jsonify({"error": "Key is required for Caesar cipher"}), 400

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
            if not key:
                return jsonify({"error": "Passphrase is required for AES"}), 400

            if action == "encrypt":
                result = encrypt_aes(text, key)
            elif action == "decrypt":
                result = decrypt_aes(text, key)
            else:
                return jsonify({"error": "Invalid action"}), 400

        # =====================
        # DES
        # =====================
        elif algorithm == "des":
            if not key:
                return jsonify({"error": "Passphrase is required for DES"}), 400

            if action == "encrypt":
                result = encrypt_des(text, key)
            elif action == "decrypt":
                result = decrypt_des(text, key)
            else:
                return jsonify({"error": "Invalid action"}), 400

        # =====================
        # 3DES
        # =====================
        elif algorithm == "3des":
            if not key:
                return jsonify({"error": "Passphrase is required for 3DES"}), 400

            if action == "encrypt":
                result = encrypt_3des(text, key)
            elif action == "decrypt":
                result = decrypt_3des(text, key)
            else:
                return jsonify({"error": "Invalid action"}), 400

        # =====================
        # Blowfish
        # =====================
        elif algorithm == "blowfish":
            if not key:
                return jsonify({"error": "Passphrase is required for Blowfish"}), 400

            if action == "encrypt":
                result = encrypt_blowfish(text, key)
            elif action == "decrypt":
                result = decrypt_blowfish(text, key)
            else:
                return jsonify({"error": "Invalid action"}), 400

        # =====================
        # RC4
        # =====================
        elif algorithm == "rc4":
            if not key:
                return jsonify({"error": "Passphrase is required for RC4"}), 400

            if action == "encrypt":
                result = encrypt_rc4(text, key)
            elif action == "decrypt":
                result = decrypt_rc4(text, key)
            else:
                return jsonify({"error": "Invalid action"}), 400

        # =====================
        # ChaCha20
        # =====================
        elif algorithm == "chacha20":
            if not key:
                return jsonify({"error": "Passphrase is required for ChaCha20"}), 400

            if action == "encrypt":
                result = encrypt_chacha20(text, key)
            elif action == "decrypt":
                result = decrypt_chacha20(text, key)
            else:
                return jsonify({"error": "Invalid action"}), 400

        # =====================
        # RSA
        # =====================
        elif algorithm == "rsa":
            if action == "generate":
                result = generate_rsa_keys()

            elif action == "encrypt":
                if not key:
                    return jsonify({"error": "Public key required"}), 400
                result = encrypt_rsa(text, key)

            elif action == "decrypt":
                if not key:
                    return jsonify({"error": "Private key required"}), 400
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

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


# ======================================================
# STEGANALYSIS API
# ======================================================
@app.route("/api/steganalysis/analyze", methods=["POST"])
def steganalysis_handler():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # Save temporarily
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, file.filename)
    file.save(file_path)

    try:
        extension = file.filename.split(".")[-1].lower()
        image_extensions = ["jpg", "jpeg", "png", "bmp", "tiff", "webp"]

        if extension in image_extensions:
            result = analyze_image(file_path)
        else:
            result = analyze_file(file_path)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# ======================================================
# APP ENTRY POINT
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)