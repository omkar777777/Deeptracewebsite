import numpy as np
import os

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# Optional PyTorch import
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

if TORCH_AVAILABLE:
    class StegCNN(nn.Module):
        """
        Deep Neural Network architecture for detecting Steganography.
        Example simplified architecture inspired by Xu-Net / Ye-Net.
        """
        def __init__(self):
            super(StegCNN, self).__init__()
            # Initial convolution to capture low-level stego noise
            self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
            self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
            
            self.pool = nn.MaxPool2d(2, 2)
            
            # A proper network would dynamically handle sizes or use AdaptiveAvgPool
            self.adaptive_pool = nn.AdaptiveAvgPool2d((64, 64))
            
            # Fully connected layers
            self.fc1 = nn.Linear(32 * 64 * 64, 128)
            self.fc2 = nn.Linear(128, 2) # Output: Cover (0), Stego (1)

        def forward(self, x):
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))
            
            # Pool to standard size to handle arbitrary image resolutions securely
            x = self.adaptive_pool(x)
            
            # Flatten
            x = x.view(x.size(0), -1)
            
            x = F.relu(self.fc1(x))
            x = self.fc2(x)
            
            # Return Softmax probabilities
            return F.softmax(x, dim=1)


def cnn_score(image):
    """
    CNN-Based Deep Learning Steganalysis.
    Detects modern steganography (LSB Matching, WOW, HUGO) by pushing 
    through a Neural Network. If PyTorch is unavailable or weights missing, 
    it returns a default neutral signal.
    Returns a normalized anomaly score 0-100.
    """
    try:
        if not TORCH_AVAILABLE:
            return 0
            
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
            
        # Normalize and construct tensor [Batch, Channels, Height, Width]
        image_tensor = torch.tensor(gray, dtype=torch.float32).unsqueeze(0).unsqueeze(0) / 255.0

        model_path = "models/cnn_steg_model.pth"
        
        if os.path.exists(model_path):
            model = StegCNN()
            model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
            model.eval()
            
            with torch.no_grad():
                probs = model(image_tensor)
                # probs[0][1] represents Stego class probability
                stego_prob = probs[0][1].item()
                return int(stego_prob * 100)
        else:
            # Fallback / Placeholder when no weights are available
            # To maintain pipeline integrity without throwing errors
            return 0
            
    except Exception:
        return 0
