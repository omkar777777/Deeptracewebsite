import os
import cv2
import numpy as np
from steganalysis.image_pipeline import analyze_image
import json

def create_test_image(path):
    # Create a random noise image which will likely trigger some statistical flags
    image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
    # Give it some smooth regions and some noisy ones
    image[:50, :50] = 128
    cv2.imwrite(path, image)

if __name__ == "__main__":
    test_path = "test_image.png"
    print("Creating test image...")
    create_test_image(test_path)
    
    print("Running analyze_image...")
    try:
        result = analyze_image(test_path)
        print("Analysis successful!")
        print(json.dumps(result, indent=4))
    except Exception as e:
        print("Error during analysis:", e)
    
    if os.path.exists(test_path):
        os.remove(test_path)
