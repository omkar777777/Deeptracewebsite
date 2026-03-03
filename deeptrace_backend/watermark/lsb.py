from PIL import Image

def embed_lsb(image, text):
    """
    Embeds a watermark signature invisibly into the Least Significant Bits (LSB).
    """
    img = image.copy()
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    # Convert text to binary string
    binary_text = ''.join(format(ord(i), '08b') for i in text)
    # Append end marker (255, 254)
    binary_text += '1111111111111110'
    
    data_len = len(binary_text)
    data_idx = 0
    
    pixels = img.load()
    width, height = img.size
    
    for y in range(height):
        for x in range(width):
            pixel = list(pixels[x, y])
            for c in range(3): # Modify R, G, B channels
                if data_idx < data_len:
                    # Clear LSB and set it to the data bit
                    pixel[c] = (pixel[c] & ~1) | int(binary_text[data_idx])
                    data_idx += 1
            pixels[x, y] = tuple(pixel)
            
            if data_idx >= data_len:
                break
        if data_idx >= data_len:
            break
            
    return img

def extract_lsb(image):
    """
    Extracts the invisible watermark signature from the LSB.
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
        
    pixels = image.load()
    width, height = image.size
    
    binary_data = ""
    extracted_text = ""
    
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            for c in range(3):
                # Extract LSB
                binary_data += str(pixel[c] & 1)
                
                if len(binary_data) == 8:
                    char_code = int(binary_data, 2)
                    extracted_text += chr(char_code)
                    binary_data = ""
                    
                    # Check for end marker
                    if extracted_text.endswith(chr(255) + chr(254)):
                        return extracted_text[:-2]
                        
    return extracted_text
