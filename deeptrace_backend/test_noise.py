import cv2
import numpy as np
from PIL import Image

from steganalysis.image_pipeline import analyze_image

def main():
    # 1. Create a dummy image full of random noise (simulating a busy photograph)
    np.random.seed(42)
    dummy_np = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    dummy_img = Image.fromarray(dummy_np, mode="RGB")
    
    # 2. Save it to disk (NO EMBEDDING HAPPENS HERE)
    dummy_img.save("test_stego_noise.png")
    
    # 3. Analyze
    result = analyze_image("test_stego_noise.png")
    print("ANALYSIS RESULT (SHOULD NOT FIND A MESSAGE):")
    print("Risk Level:", result.get("risk_level"))
    print("Score:", result.get("total_score"))
    print("Found hidden content:", result.get("hidden_content_found"))

if __name__ == "__main__":
    main()
