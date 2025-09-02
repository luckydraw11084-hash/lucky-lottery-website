#!/usr/bin/env python3
"""
Setup script for Lucky Draw Application
Installs dependencies and generates UPI QR codes
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def generate_qr_codes():
    """Generate UPI QR codes"""
    print("🎯 Generating UPI QR codes...")
    
    try:
        # Import and run QR code generation
        from generate_qr import generate_static_qr
        
        # Generate static QR code
        qr_path = generate_static_qr()
        print(f"✅ QR code generated: {qr_path}")
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import QR generation module: {e}")
        print("   Make sure qrcode and Pillow are installed")
        return False
    except Exception as e:
        print(f"❌ Failed to generate QR codes: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        'data',
        'static/images',
        'templates'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ Created: {directory}/")
    
    return True

def main():
    """Main setup function"""
    print("🎯 Lucky Draw Application Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version.split()[0]}")
    
    # Create directories
    if not create_directories():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Generate QR codes
    if not generate_qr_codes():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Run: python app.py")
    print("   2. Open: http://localhost:5000")
    print("   3. Test the UPI payment system")
    print("\n💡 The QR code is now available at: static/images/upi_qr_static.png")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
