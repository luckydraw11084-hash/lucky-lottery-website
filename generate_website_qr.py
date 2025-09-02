#!/usr/bin/env python3
"""
QR Code Generator for Lucky Draw Website
This script generates a QR code that when scanned, opens your Lucky Draw website
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import socket

def get_local_ip():
    """Get the local IP address of the computer"""
    try:
        # Connect to a remote address to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "localhost"

def generate_website_qr():
    """Generate QR code for the Lucky Draw website"""
    
    # Get local IP address for mobile access
    local_ip = get_local_ip()
    website_url = f"http://{local_ip}:5000"
    
    print(f"🌐 Using IP address: {local_ip}")
    print(f"📱 Mobile devices can access: {website_url}")
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    # Add data to QR code
    qr.add_data(website_url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to PIL Image for editing
    qr_pil = qr_image.convert('RGBA')
    
    # Create a larger canvas for the logo and text
    canvas_size = (400, 500)
    # Use warm beige background matching the image
    canvas = Image.new('RGBA', canvas_size, (253, 251, 246, 255))  # Warm beige background
    
    # Calculate positions
    qr_size = 300
    qr_x = (canvas_size[0] - qr_size) // 2
    qr_y = 50
    
    # Resize QR code
    qr_resized = qr_pil.resize((qr_size, qr_size))
    
    # Paste QR code onto canvas
    canvas.paste(qr_resized, (qr_x, qr_y), qr_resized)
    
    # Add text
    draw = ImageDraw.Draw(canvas)
    
    # Try to use a default font, fallback to basic if not available
    try:
        # Try to use a system font
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 16)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Add title with warm brown color
    title = "Lucky Draw"
    title_bbox = draw.textbbox((0, 0), title, font=font_large)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (canvas_size[0] - title_width) // 2
    draw.text((title_x, 10), title, fill=(92, 58, 33, 255), font=font_large)  # Warm brown
    
    # Add subtitle
    subtitle = "Scan to Join!"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (canvas_size[0] - subtitle_width) // 2
    draw.text((subtitle_x, 370), subtitle, fill=(92, 58, 33, 255), font=font_small)  # Warm brown
    
    # Add URL
    url_text = website_url
    url_bbox = draw.textbbox((0, 0), url_text, font=font_small)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (canvas_size[0] - url_width) // 2
    draw.text((url_x, 390), url_text, fill=(139, 111, 92, 255), font=font_small)  # Lighter brown
    
    # Add instructions
    instructions = "Scan with any QR app"
    inst_bbox = draw.textbbox((0, 0), instructions, font=font_small)
    inst_width = inst_bbox[2] - inst_bbox[0]
    inst_x = (canvas_size[0] - inst_width) // 2
    draw.text((inst_x, 420), instructions, fill=(139, 111, 92, 255), font=font_small)  # Lighter brown
    
    # Save the QR code
    output_path = "static/images/website_qr.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    canvas.save(output_path)
    
    print(f"✅ QR Code generated successfully!")
    print(f"📁 Saved to: {output_path}")
    print(f"🌐 Website URL: {website_url}")
    print(f"📱 Scan this QR code with any mobile app to open your website!")
    print(f"💡 Make sure your computer and phone are on the same WiFi network!")
    
    return output_path

def generate_simple_qr():
    """Generate a simple QR code without styling"""
    local_ip = get_local_ip()
    website_url = f"http://{local_ip}:5000"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    
    qr.add_data(website_url)
    qr.make(fit=True)
    
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    output_path = "static/images/website_qr_simple.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    qr_image.save(output_path)
    
    print(f"✅ Simple QR Code generated: {output_path}")
    return output_path

if __name__ == "__main__":
    try:
        # Try to generate styled QR code
        generate_website_qr()
    except Exception as e:
        print(f"⚠️  Styled QR generation failed: {e}")
        print("🔄 Generating simple QR code instead...")
        generate_simple_qr()
    
    print("\n🎯 How to use:")
    print("1. Save the QR code image")
    print("2. Print it or display it on your phone/computer")
    print("3. Anyone can scan it to open your Lucky Draw website")
    print("4. Make sure all devices are on the same WiFi network")
    print("5. When you deploy to a real domain, update the URL in the script")
