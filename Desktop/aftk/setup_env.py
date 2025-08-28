#!/usr/bin/env python3
"""
Setup script for RentPay USSD M-Pesa integration
This script helps you create the .env file with your M-Pesa credentials
"""

import os

def create_env_file():
    """Create .env file with M-Pesa credentials"""
    
    print("🏠 RentPay USSD - M-Pesa Setup")
    print("=" * 40)
    print()
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/N): ").lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    print("Please enter your M-Pesa API credentials:")
    print()
    
    # Get credentials from user
    consumer_key = input("M-Pesa Consumer Key: ").strip()
    consumer_secret = input("M-Pesa Consumer Secret: ").strip()
    shortcode = input("M-Pesa Shortcode: ").strip()
    passkey = input("M-Pesa Passkey: ").strip()
    
    # Environment selection
    print("\nSelect environment:")
    print("1. Sandbox (for testing)")
    print("2. Production")
    env_choice = input("Enter choice (1 or 2): ").strip()
    
    sandbox = "true" if env_choice == "1" else "false"
    
    # Callback URL
    callback_url = input("Callback URL (press Enter for default): ").strip()
    if not callback_url:
        callback_url = "http://localhost:5000/mpesa/callback"
    
    # Create .env content
    env_content = f"""# M-Pesa API Credentials
MPESA_CONSUMER_KEY={consumer_key}
MPESA_CONSUMER_SECRET={consumer_secret}
MPESA_SHORTCODE={shortcode}
MPESA_PASSKEY={passkey}

# M-Pesa Environment (true for sandbox, false for production)
MPESA_SANDBOX={sandbox}

# Callback URL for payment notifications
MPESA_CALLBACK_URL={callback_url}
"""
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print(f"📁 File location: {os.path.abspath('.env')}")
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: python ussd.py")
        print("3. Test the payment flow")
        
    except Exception as e:
        print(f"\n❌ Error creating .env file: {str(e)}")

def check_setup():
    """Check if setup is complete"""
    print("🔍 Checking setup status...")
    print()
    
    # Check .env file
    if os.path.exists('.env'):
        print("✅ .env file exists")
        
        # Load and check environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            'MPESA_CONSUMER_KEY',
            'MPESA_CONSUMER_SECRET',
            'MPESA_SHORTCODE',
            'MPESA_PASSKEY'
        ]
        
        missing_vars = []
        for var in required_vars:
            if os.getenv(var):
                print(f"✅ {var}: Set")
            else:
                print(f"❌ {var}: Not set")
                missing_vars.append(var)
        
        if missing_vars:
            print(f"\n⚠️  Missing variables: {', '.join(missing_vars)}")
            print("Run setup again to configure missing variables.")
        else:
            print("\n🎉 Setup is complete! All required variables are configured.")
            
    else:
        print("❌ .env file not found")
        print("Run setup to create the .env file with your M-Pesa credentials.")

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Setup M-Pesa credentials (create .env file)")
    print("2. Check setup status")
    print("3. Exit")
    
    choice = input("\nEnter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        create_env_file()
    elif choice == "2":
        check_setup()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice. Please run the script again.")
