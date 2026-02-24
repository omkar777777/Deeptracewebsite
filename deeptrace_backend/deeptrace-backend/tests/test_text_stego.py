from stego.text.zerowidth import embed_zerowidth, extract_zerowidth

cover = "This is a simple cover text for testing."
secret = "HELLO"

stego = embed_zerowidth(cover, secret)
extracted = extract_zerowidth(stego)

assert extracted == secret
print("✅ Zero-width test passed")