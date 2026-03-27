import cv2
import numpy as np
from steganalysis.image_pipeline import analyze_image

# Create a dummy image
dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
cv2.imwrite("dummy.png", dummy_image)

try:
    result = analyze_image("dummy.png")
    print("Success:", result)
except Exception as e:
    import traceback
    traceback.print_exc()
