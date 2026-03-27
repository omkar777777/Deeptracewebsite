try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

import numpy as np

# Optional scikit-learn import
try:
    import joblib
    # from sklearn.ensemble import RandomForestClassifier
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning)
except Exception:
    pass

def residual_filter(image):
    """
    Applies a basic high-pass filter (prediction error) to extract local residuals.
    This simulates the extraction of noise components common in SRM.
    """
    # Simple edge-prediction kernel
    kernel = np.array([
        [ 0, -1,  0],
        [-1,  4, -1],
        [ 0, -1,  0]
    ])
    
    residual = cv2.filter2D(image, -1, kernel)
    return residual

def extract_srm_features(residual):
    """
    Simulates feature extraction.
    True SRM extracts ~34k co-occurrence features. We simulate by computing
    a basic histogram distribution of the noise residuals.
    """
    hist = np.histogram(residual.flatten(), bins=256, range=(0, 256))[0]
    # Normalize
    hist_norm = hist / (np.sum(hist) + 1e-7)
    return hist_norm

def srm_score(image):
    """
    Spatial Rich Model (SRM) Feature-Based Analysis.
    Attempts to use a trained ML classifier (e.g., Random Forest) to evaluate 
    extracted features. If a model is not found, it reverts to a heuristic 
    anomaly estimation based on residual noise variance.
    Returns a normalized anomaly score 0-100.
    """
    try:
        # 1. Convert to grayscale if it's color
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
            
        # 2. Extract residuals
        residual = residual_filter(gray)
        
        # 3. Extract features
        features = extract_srm_features(residual)
        
        # 4. Attempt ML inference (assuming model exists locally)
        model_path = "models/srm_classifier.pkl"
        
        try:
            model = joblib.load(model_path)
            # prediction yields probabilities: [P(Cover), P(Stego)]
            probs = model.predict_proba([features])[0]
            stego_prob = probs[1]
            return min(int(stego_prob * 100), 100)
            
        except Exception:
            # Fallback heuristic: High residual noise variance often implies LSB alteration
            # This is a proxy estimation for demonstration and pipeline completeness
            variance = np.var(residual)
            
            # Typical natural images might have certain variance ranges depending on texture
            # A completely flat heuristic isn't perfect, but we translate variance to a 0-100 scale
            # bounded arbitrarily for demonstration.
            heuristic_prob = min(variance / 2000.0, 1.0) 
            score = int(heuristic_prob * 100)
            # dampen the heuristic since it's just a proxy
            return min(max(score - 20, 0), 100)

    except Exception:
        return 0
