import requests
import json

URL = "http://localhost:5000/api/crypto"

def test_api(algo, action, text, key=None):
    payload = {
        "algorithm": algo,
        "action": action,
        "text": text
    }
    if key:
        payload["key"] = key
        
    try:
        response = requests.post(URL, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def test_rsa_keygen():
    payload = {
        "algorithm": "rsa",
        "action": "generate"
    }
    try:
        response = requests.post(URL, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

print("=== DEEPTRACE CRYPTO API TEST ===")
try:
    # 1. Test ChaCha20
    plaintext = "HelloWorld123"
    chacha_key = "12345678901234567890123456789012" # 32 bytes
    
    print("\n[Tested] ChaCha20")
    enc_res = test_api("chacha20", "encrypt", plaintext, chacha_key)
    if "result" in enc_res:
        ciphertext = enc_res["result"]
        print(f"  Encrypt: {plaintext} -> {ciphertext[:20]}...")
        
        dec_res = test_api("chacha20", "decrypt", ciphertext, chacha_key)
        if "result" in dec_res:
            print(f"  Decrypt matches original: {dec_res['result'] == plaintext}")
        else:
            print(f"  Decrypt failed: {dec_res}")
    else:
        print(f"  Encrypt failed: {enc_res}")
        
    # 2. Test RSA
    print("\n[Tested] RSA")
    kg_res = test_rsa_keygen()
    if "result" in kg_res:
        keys = kg_res["result"]
        pub = keys["public_key"]
        priv = keys["private_key"]
        print("  KeyGen: SUCCESS")
        
        enc_res = test_api("rsa", "encrypt", plaintext, pub)
        if "result" in enc_res:
            ciphertext = enc_res["result"]
            print(f"  Encrypt: {plaintext} -> {ciphertext[:20]}...")
            
            dec_res = test_api("rsa", "decrypt", ciphertext, priv)
            if "result" in dec_res:
                print(f"  Decrypt matches original: {dec_res['result'] == plaintext}")
            else:
                print(f"  Decrypt failed: {dec_res}")
        else:
            print(f"  Encrypt failed: {enc_res}")
    else:
        print(f"  KeyGen failed: {kg_res}")
except Exception as e:
    print(f"API Testing failed. Is the server running? {e}")
