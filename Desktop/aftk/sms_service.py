import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SMSService:
    def __init__(self):
        # SMS API Configuration - using Africa's Talking as default
        self.api_key = os.getenv('SMS_API_KEY', '')
        self.username = os.getenv('SMS_USERNAME', '')
        self.sender_id = os.getenv('SMS_SENDER_ID', 'RENTPAY')
        self.api_url = os.getenv('SMS_API_URL', 'https://api.africastalking.com/version1/messaging')
        
        # Alternative SMS providers
        self.provider = os.getenv('SMS_PROVIDER', 'africastalking').lower()
        
    def send_rent_invoice(self, tenant_phone: str, tenant_name: str, house_number: str, 
                          estate: str, rent_amount: int, due_date: str, ussd_code: str) -> dict:
        """Send rent invoice SMS to tenant"""
        
        # Format the SMS message
        message = self._format_rent_invoice(
            tenant_name, house_number, estate, rent_amount, due_date, ussd_code
        )
        
        try:
            if self.provider == 'africastalking':
                return self._send_africastalking(tenant_phone, message)
            elif self.provider == 'twilio':
                return self._send_twilio(tenant_phone, message)
            else:
                return self._send_generic(tenant_phone, message)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to send SMS"
            }
    
    def _format_rent_invoice(self, tenant_name: str, house_number: str, estate: str, 
                            rent_amount: int, due_date: str, ussd_code: str) -> str:
        """Format the rent invoice SMS message"""
        
        message = f"""RENT INVOICE
        
Dear {tenant_name},
House: {house_number}
Estate: {estate}
Rent Due: KES {rent_amount:,}
Due Date: {due_date}

To pay, dial: {ussd_code}

Thank you,
RentPay Team"""
        
        return message
    
    def _send_africastalking(self, phone: str, message: str) -> dict:
        """Send SMS using Africa's Talking API"""
        try:
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'apiKey': self.api_key
            }
            
            data = {
                'username': self.username,
                'to': phone,
                'message': message,
                'from': self.sender_id
            }
            
            response = requests.post(self.api_url, headers=headers, data=data)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "message_id": result.get('SMSMessageData', {}).get('Recipients', [{}])[0].get('messageId'),
                "provider": "Africa's Talking",
                "status": "sent"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": "Africa's Talking"
            }
    
    def _send_twilio(self, phone: str, message: str) -> dict:
        """Send SMS using Twilio API"""
        try:
            # Twilio configuration
            account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
            auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
            twilio_number = os.getenv('TWILIO_PHONE_NUMBER', '')
            
            if not all([account_sid, auth_token, twilio_number]):
                raise Exception("Twilio credentials not configured")
            
            url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
            
            data = {
                'To': phone,
                'From': twilio_number,
                'Body': message
            }
            
            response = requests.post(url, data=data, auth=(account_sid, auth_token))
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "message_id": result.get('sid'),
                "provider": "Twilio",
                "status": "sent"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": "Twilio"
            }
    
    def _send_generic(self, phone: str, message: str) -> dict:
        """Generic SMS sending (for testing or custom providers)"""
        try:
            # For testing purposes, just log the message
            print(f"=== SMS TO BE SENT ===")
            print(f"To: {phone}")
            print(f"Message: {message}")
            print(f"======================")
            
            return {
                "success": True,
                "message_id": f"test_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "provider": "Generic/Test",
                "status": "logged"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": "Generic/Test"
            }
    
    def send_bulk_invoices(self, tenants_data: list, ussd_code: str) -> dict:
        """Send rent invoices to multiple tenants"""
        results = []
        success_count = 0
        failure_count = 0
        
        for tenant in tenants_data:
            result = self.send_rent_invoice(
                tenant_phone=tenant['phone'],
                tenant_name=tenant['name'],
                house_number=tenant['house_number'],
                estate=tenant['estate'],
                rent_amount=tenant['rent_amount'],
                due_date=tenant['due_date'],
                ussd_code=ussd_code
            )
            
            results.append({
                'tenant': tenant['name'],
                'phone': tenant['phone'],
                'result': result
            })
            
            if result['success']:
                success_count += 1
            else:
                failure_count += 1
        
        return {
            "total_sent": len(tenants_data),
            "success_count": success_count,
            "failure_count": failure_count,
            "results": results
        }
