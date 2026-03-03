from PIL import Image, ImageDraw, ImageFont

def embed_visible(image, text, opacity=0.5, position="bottom_right"):
    """
    Embeds a visible watermark onto the image using alpha blending.
    Formula: Iw = alpha * I + (1 - alpha) * W
    visualized as alpha_composite in PIL for text overlays.
    """
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
        
    # Make a blank image for the text, initialized to transparent
    txt_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
    
    # Try to load a reasonable font
    try:
        # Size font relative to image height
        font_size = max(int(image.height / 15), 20)
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        
    draw = ImageDraw.Draw(txt_layer)
    
    # Get text size
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        # Pillow fallback
        text_width, text_height = draw.textsize(text, font=font)
        
    width, height = image.size
    
    # Calculate position
    if position == "bottom_right":
        x = width - text_width - 20
        y = height - text_height - 20
    elif position == "center":
        x = (width - text_width) // 2
        y = (height - text_height) // 2
    elif position == "top_left":
        x = 20
        y = 20
    else:
        x = width - text_width - 20
        y = height - text_height - 20
        
    x = max(0, x)
    y = max(0, y)
        
    # Apply opacity (alpha value 0-255)
    # The formula uses alpha as the weight for blending.
    opacity_int = int(255 * opacity)
    
    # Draw text
    draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity_int))
    
    # Alpha composite
    watermarked_image = Image.alpha_composite(image, txt_layer)
    return watermarked_image.convert("RGB") # Return RGB to avoid PNG transparency weirdness when unexpected
