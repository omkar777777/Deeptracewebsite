from flask import Flask, request, jsonify
from flask_cors import CORS

# ------------------------------
# Cryptography imports
# ------------------------------
from crypto.caesar import encrypt_caesar, decrypt_caesar
from crypto.aes import encrypt_aes, decrypt_aes
from crypto.des import encrypt_des, decrypt_des
from crypto.tripledes import encrypt_3des, decrypt_3des
from crypto.blowfish import encrypt_blowfish, decrypt_blowfish
from crypto.rc4 import encrypt_rc4, decrypt_rc4
from crypto.chacha20 import encrypt_chacha20, decrypt_chacha20
from crypto.rsa import generate_rsa_keys, encrypt_rsa, decrypt_rsa

# ------------------------------
# Steganography routes
# ------------------------------
from routes.stego_routes import stego_bp

# ------------------------------
# App initialization
# ------------------------------
app = Flask(__name__)
CORS(app)  # Allow requests from frontend (React)

# ------------------------------
# Register Blueprints
# ------------------------------
app.register_blueprint(stego_bp)
from watermark.routes import watermark_bp
app.register_blueprint(watermark_bp)


# ======================================================
# CRYPTOGRAPHY API
# ======================================================
@app.route("/api/crypto", methods=["POST"])
def crypto_handler():
    """
    Unified Cryptography API endpoint

    Expected JSON:
    {
        algorithm: "caesar" | "aes" | "des" | "3des" | "blowfish" | "rc4" | "chacha20" | "rsa"
        action: "encrypt" | "decrypt" | "generate"
        text: string
        key: string | number (if required)
    }
    """

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
        # AES (256-bit, CBC)
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
        # DES (56-bit, CBC)
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
        # 3DES (Triple DES)
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
        # Blowfish (CBC)
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
        # RC4 (Stream Cipher)
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
        # ChaCha20 (Modern Stream Cipher)
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
        # RSA (2048-bit)
        # =====================
        elif algorithm == "rsa":
            if action == "generate":
                result = generate_rsa_keys()

            elif action == "encrypt":
                if not key:
                    return jsonify(
                        {"error": "Public key is required for RSA encryption"}), 400
                result = encrypt_rsa(text, key)

            elif action == "decrypt":
                if not key:
                    return jsonify(
                        {"error": "Private key is required for RSA decryption"}), 400
                result = decrypt_rsa(text, key)

            else:
                return jsonify({"error": "Invalid RSA action"}), 400

        # =====================
        # Unsupported Algorithm
        # =====================
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
# APP ENTRY POINT
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)