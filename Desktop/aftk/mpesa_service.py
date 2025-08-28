import base64
import hashlib
import time
import requests
from datetime import datetime
from cryptography.fernet import Fernet
from config import Config

class MpesaService:
    def __init__(self):
        self.config = Config()
        # Generate a key for encryption (in production, store this securely)
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
        self.access_token_cache = {}
    
    def generate_access_token(self, consumer_key: str, consumer_secret: str, integration_id: str) -> str:
        """Generate M-Pesa access token with caching"""
        cache_key = f'access_token_{integration_id}'
        
        # Check if we have a cached token
        if cache_key in self.access_token_cache:
            cached_data = self.access_token_cache[cache_key]
            if time.time() < cached_data['expires_at']:
                return cached_data['token']
        
        # Generate new token
        try:
            response = requests.get(
                self.config.MPESA_OAUTH_URL,
                auth=(consumer_key, consumer_secret),
                headers={'Accept': 'application/json'},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            print(f"OAuth response: {data}")
            
            access_token = data.get('access_token')
            expires_in = data.get('expires_in', 3600)
            
            # Convert expires_in to integer if it's a string
            if isinstance(expires_in, str):
                try:
                    expires_in = int(expires_in)
                except ValueError:
                    expires_in = 3600  # Default fallback
                    print(f"Warning: Could not convert expires_in '{data.get('expires_in')}' to int, using default: {expires_in}")
            
            if not access_token:
                raise Exception("No access token received from M-Pesa OAuth")
            
            # Cache the token (expires at 80% of actual expiry time)
            cache_duration = int(expires_in * 0.8)
            self.access_token_cache[cache_key] = {
                'token': access_token,
                'expires_at': time.time() + cache_duration
            }
            
            return access_token
            
        except requests.RequestException as e:
            print(f"Request error generating access token: {str(e)}")
            raise Exception(f"Failed to generate access token: {str(e)}")
        except Exception as e:
            print(f"Error generating access token: {str(e)}")
            raise Exception(f"Access token generation failed: {str(e)}")
    
    def generate_password(self, shortcode: str, passkey: str) -> str:
        """Generate M-Pesa password using timestamp"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_string = f"{shortcode}{passkey}{timestamp}"
        password = base64.b64encode(password_string.encode()).decode()
        print(f"Generated password with timestamp: {timestamp}")
        return password
    
    def send_stk_push(self, phone: str, amount: int, account_ref: str, description: str) -> dict:
        """Send STK push to initiate M-Pesa payment"""
        try:
            print(f"Starting STK push for phone: {phone}, amount: {amount}")
            
            # Generate access token
            access_token = self.generate_access_token(
                self.config.MPESA_CONSUMER_KEY,
                self.config.MPESA_CONSUMER_SECRET,
                'default'
            )
            print(f"Access token generated successfully")
            
            # Generate password
            password = self.generate_password(self.config.MPESA_SHORTCODE, self.config.MPESA_PASSKEY)
            
            # Prepare request body
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            
            payload = {
                'BusinessShortCode': self.config.MPESA_SHORTCODE,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': amount,
                'PartyA': phone,
                'PartyB': self.config.MPESA_SHORTCODE,
                'PhoneNumber': phone,
                'CallBackURL': self.config.MPESA_CALLBACK_URL,
                'AccountReference': account_ref,
                'TransactionDesc': description[:13]  # Limit to 13 characters
            }
            
            print(f"STK push payload: {payload}")
            
            # Send STK push request
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            
            print(f"Sending STK push to: {self.config.MPESA_STK_PUSH_URL}")
            response = requests.post(
                self.config.MPESA_STK_PUSH_URL,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            # Log the full response for debugging
            print(f"STK push response status: {response.status_code}")
            print(f"STK push response headers: {dict(response.headers)}")
            
            if not response.ok:
                error_detail = response.text
                print(f"STK push error response: {error_detail}")
                try:
                    error_json = response.json()
                    print(f"STK push error JSON: {error_json}")
                except:
                    pass
                response.raise_for_status()
            
            result = response.json()
            print(f"STK push response: {result}")
            
            return result
            
        except requests.RequestException as e:
            print(f"Request error in STK push: {str(e)}")
            raise Exception(f"Failed to send STK push: {str(e)}")
        except Exception as e:
            print(f"STK push error: {str(e)}")
            raise Exception(f"STK push error: {str(e)}")
    
    def format_phone_number(self, phone: str) -> str:
        """Format phone number for M-Pesa (add 254 prefix if needed)"""
        if phone.startswith('+'):
            phone = phone[1:]
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        if not phone.startswith('254'):
            phone = '254' + phone
        return phone
