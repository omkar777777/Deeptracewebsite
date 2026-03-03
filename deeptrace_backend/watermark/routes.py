from flask import Blueprint, request, jsonify
from PIL import Image
import io
import base64
from .dct import embed_dct, extract_dct
from .dwt import embed_dwt, extract_dwt

watermark_bp = Blueprint('watermark', __name__)

def image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def base64_to_image(base64_string):
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    img_data = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(img_data))

@watermark_bp.route("/api/watermark/embed", methods=["POST"])
def embed():
    try:
        data = request.json
        image_data = data.get("image")
        watermark_type = data.get("type")
        secret_key = data.get("secretKey", "")
        text = data.get("text")
        opacity = float(data.get("opacity", 0.5))
        
        if not image_data or not watermark_type or not text:
            return jsonify({"error": "Missing required fields"}), 400
            
        image = base64_to_image(image_data)
        
        if watermark_type == "invisible_dct":
            result_image = embed_dct(image, secret_key, text)
        elif watermark_type == "invisible_dwt":
            result_image = embed_dwt(image, secret_key, text)
        elif watermark_type == "visible":
            from .visible import embed_visible
            result_image = embed_visible(image, text, opacity=opacity)
        elif watermark_type == "invisible_lsb":
            from .lsb import embed_lsb
            result_image = embed_lsb(image, text)
        else:
            return jsonify({"error": "Invalid watermark type"}), 400
            
        return jsonify({
            "dataUrl": image_to_base64(result_image),
            "message": "Watermark applied successfully"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@watermark_bp.route("/api/watermark/extract", methods=["POST"])
def extract():
    try:
        data = request.json
        image_data = data.get("image")
        watermark_type = data.get("type")
        secret_key = data.get("secretKey", "")
        
        if not image_data or not watermark_type:
            return jsonify({"error": "Missing required fields"}), 400
            
        image = base64_to_image(image_data)
        
        if watermark_type == "invisible_dct":
            extracted_text = extract_dct(image, secret_key)
        elif watermark_type == "invisible_dwt":
            extracted_text = extract_dwt(image, secret_key)
        elif watermark_type == "invisible_lsb":
            from .lsb import extract_lsb
            extracted_text = extract_lsb(image)
        elif watermark_type == "visible":
            return jsonify({"error": "Extracting from visible watermark is not supported"}), 400
        else:
            return jsonify({"error": "Invalid watermark type"}), 400
            
        return jsonify({
            "data": {
                "message": extracted_text 
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
