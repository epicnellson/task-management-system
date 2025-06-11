from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size):
    # Create a new image with a white background
    image = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a blue circle
    circle_color = '#007bff'
    draw.ellipse([size*0.1, size*0.1, size*0.9, size*0.9], fill=circle_color)
    
    # Add text
    text = "TM"
    try:
        font_size = int(size * 0.4)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill='white', font=font)
    
    return image

def generate_icons():
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    # Create icons directory if it doesn't exist
    if not os.path.exists('app/static/icons'):
        os.makedirs('app/static/icons')
    
    for size in sizes:
        icon = create_icon(size)
        icon.save(f'app/static/icons/icon-{size}x{size}.png')

if __name__ == '__main__':
    generate_icons() 