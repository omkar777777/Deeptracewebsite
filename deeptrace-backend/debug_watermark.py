import hashlib
import base64
import io
import numpy as np
from PIL import Image
from watermark.dct import embed_dct, extract_dct
from watermark.dwt import embed_dwt, extract_dwt

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

def test_full_pipeline(name, embed_func, extract_func):
    print(f"--- Testing {name} Pipeline ---")
    
    # 1. Create Source Image (RGB Random) - USING ODD SIZE TO TRIGGER PADDING/CROP BUG
    arr = np.random.randint(0, 256, (257, 257, 3), dtype=np.uint8)
    original_img = Image.fromarray(arr).convert("RGB")
    
    secret_key = "debug_key"
    payload = '{"id":"user_1","ts":123456789,"hash":"abc"}'
    
    try:
        # 2. Embed
        print("1. Embedding...")
        watermarked_img = embed_func(original_img, secret_key, payload)
        
        # 3. Simulate Backend Response (Image -> Base64)
        print("2. Server: Converting to Base64...")
        b64_string = image_to_base64(watermarked_img)
        
        # 4. Simulate Client Download & Upload (Base64 -> Image)
        # This includes saving to PNG (lossless) inside the base64 conversion
        print("3. Client: Uploading (Base64 -> Image)...")
        uploaded_img = base64_to_image(b64_string)
        
        # Check if pixels changed due to RGB->YCbCr->RGB
        # We can't easily check 'arr' vs 'uploaded_img' because watermark changed it.
        # But we can assume 'uploaded_img' is what the extractor gets.
        
        # 5. Extract
        print("4. Extracting...")
        extracted_text = extract_func(uploaded_img, secret_key)
        
        print(f"Original Payload: {payload}")
        print(f"Extracted Data:   {extracted_text}")
        
        if payload == extracted_text:
            print(f"SUCCESS: {name} survived the pipeline!")
        else:
            print(f"FAILURE: {name} data mismatch.")
            # Check partial match
            if payload[:10] in extracted_text:
                print("PARTIAL: Some data recovered.")
            else:
                print("TOTAL FAILURE: Garbage output.")
                
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    with open("debug_output_pipeline.txt", "w") as f:
        import sys
        sys.stdout = f
        print("STARTING PIPELINE DEBUG")
        test_full_pipeline("DCT", embed_dct, extract_dct)
        print("\n")
        test_full_pipeline("DWT", embed_dwt, extract_dwt)
        print("DEBUG COMPLETE")
