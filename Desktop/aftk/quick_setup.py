#!/usr/bin/env python3
"""
Quick Setup Script for RentPay
This script helps developers get up and running quickly
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists('.env'):
        print("📝 Creating .env file from template...")
        try:
            with open('env_template.txt', 'r') as template:
                content = template.read()
            with open('.env', 'w') as env_file:
                env_file.write(content)
            print("✅ .env file created successfully")
            print("⚠️  Please edit .env file with your actual credentials")
            return True
        except FileNotFoundError:
            print("❌ env_template.txt not found")
            return False
    else:
        print("✅ .env file already exists")
        return True

def main():
    print("🚀 RentPay Quick Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        print("❌ Failed to create .env file")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your M-Pesa and SMS credentials")
    print("2. Run USSD app: python ussd.py")
    print("3. Run Dashboard: python landlord_dashboard.py")
    print("4. Visit dashboard: http://localhost:5001")
    print("\n📚 Documentation: README.md and SMS_README.md")

if __name__ == "__main__":
    main()
