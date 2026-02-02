from stego.text.zerowidth import embed_zerowidth, extract_zerowidth

cover = "This is a test sentence used for zero width steganography"
secret = "hi"

stego = embed_zerowidth(cover, secret)

print("Cover length:", len(cover))
print("Stego length:", len(stego))
print("Hidden chars added:", len(stego) - len(cover))

extracted = extract_zerowidth(stego)
print("Extracted message:", extracted)