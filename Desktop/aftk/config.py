import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # M-Pesa Configuration
    MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY', '')
    MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET', '')
    MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE', '')
    MPESA_PASSKEY = os.getenv('MPESA_PASSKEY', '')
    
    # M-Pesa API URLs
    MPESA_SANDBOX = os.getenv('MPESA_SANDBOX', 'true').lower() == 'true'
    
    if MPESA_SANDBOX:
        MPESA_BASE_URL = 'https://sandbox.safaricom.co.ke'
    else:
        MPESA_BASE_URL = 'https://api.safaricom.co.ke'
    
    MPESA_OAUTH_URL = f'{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials'
    MPESA_STK_PUSH_URL = f'{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest'
    
    # Callback URL for payment notifications
    MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL', 'http://localhost:5000/mpesa/callback')
    
    # Cache settings
    ACCESS_TOKEN_CACHE_DURATION = 3600  # 1 hour in seconds
