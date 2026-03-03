import cv2
import numpy as np
from PIL import Image

from stego.image.lsb import embed_lsb
from steganalysis.image_pipeline import analyze_image

def main():
    # 1. Create a dummy PIL image to embed into
    dummy_np = np.zeros((100, 100, 3), dtype=np.uint8)
    dummy_img = Image.fromarray(dummy_np, mode="RGB")
    
    # 2. Embed secret data
    secret = "Hello DeepTrace!"
    stego_img = embed_lsb(dummy_img, secret)
    
    # 3. Save it to disk so we can analyze it (simulate upload path)
    stego_img.save("test_stego.png")
    
    # 4. Analyze
    result = analyze_image("test_stego.png")
    print("ANALYSIS RESULT:")
    print("Risk Level:", result.get("risk_level"))
    print("Score:", result.get("total_score"))
    print("Found hidden content:", result.get("hidden_content_found"))
    print("Extracted Data:", result.get("extracted_content"))

if __name__ == "__main__":
    main()
