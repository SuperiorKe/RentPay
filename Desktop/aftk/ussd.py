import os
from flask import Flask, request, jsonify
from mpesa_service import MpesaService

app = Flask(__name__)

# Initialize M-Pesa service
try:
    mpesa_service = MpesaService()
    mpesa_available = True
except Exception as e:
    print(f"M-Pesa service initialization failed: {str(e)}")
    mpesa_available = False

# Mock tenant database - in production, this would connect to a real database
TENANT_DB = {
    "+254792138852": {
        "name": "John",
        "house_number": "HSe no. 4",
        "estate": "Killimani estate",
        "rent_due": 5,
        "last_payment": "2024-01-15"
    },
    "+254715035359": {
        "name": "Kenn",
        "house_number": "HSe no. 12",
        "estate": "Westlands",
        "rent_due": 30000,
        "last_payment": "2024-01-10"
    }
}

@app.route("/ussd", methods=['POST'])
def ussd():
    # Read the variables sent via POST from our API
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    if text == '':
        # Welcome screen with personalized tenant information
        tenant = TENANT_DB.get(phone_number, None)
        if tenant:
            response = f"CON Welcome, {tenant['name']}. {tenant['house_number']}, {tenant['estate']}\n\n"
            response += "1. Check dues\n"
            response += "2. Pay rent\n"
            response += "0. Exit"
        else:
            # New tenant registration flow
            response = "CON Welcome to RentPay USSD\n\n"
            response += "1. Register as tenant\n"
            response += "0. Exit"

    elif text == '1':
        # Check dues option
        tenant = TENANT_DB.get(phone_number, None)
        if tenant:
            response = f"CON Your rent details:\n\n"
            response += f"Rent due: KES {tenant['rent_due']:,}\n"
            response += f"Last payment: {tenant['last_payment']}\n\n"
            response += "1. Back to main menu\n"
            response += "0. Exit"
        else:
            response = "END Tenant not found. Please register first."

    elif text == '2':
        # Pay rent option - only full amount
        tenant = TENANT_DB.get(phone_number, None)
        if tenant:
            response = f"CON Pay Full Rent\n\n"
            response += f"Amount to pay: KES {tenant['rent_due']:,}\n\n"
            response += "1. Confirm payment\n"
            response += "2. Back to main menu\n"
            response += "0. Exit"
        else:
            response = "END Tenant not found. Please register first."

    elif text == '0':
        # Exit option
        response = "END Thank you for using RentPay USSD. Goodbye!"

    elif text == '1*1':
        # Back to main menu from check dues
        tenant = TENANT_DB.get(phone_number, None)
        if tenant:
            response = f"CON Welcome, {tenant['name']}. {tenant['house_number']}, {tenant['estate']}\n\n"
            response += "1. Check dues\n"
            response += "2. Pay rent\n"
            response += "0. Exit"
        else:
            response = "END Session expired. Please dial again."

    elif text == '2*1':
        # Confirm payment - show payment methods
        response = "CON Payment Method:\n\n"
        response += "1. M-Pesa\n"
        response += "2. Airtel Money\n"
        response += "#. Back to payment menu\n"
        response += "0. Exit"

    elif text == '2*2':
        # Back to main menu from payment
        tenant = TENANT_DB.get(phone_number, None)
        if tenant:
            response = f"CON Welcome, {tenant['name']}. {tenant['house_number']}, {tenant['estate']}\n\n"
            response += "1. Check dues\n"
            response += "2. Pay rent\n"
            response += "0. Exit"
        else:
            response = "END Session expired. Please dial again."

    elif text == '2*1*1':
        # M-Pesa payment - initiate STK push
        tenant = TENANT_DB.get(phone_number, None)
        if tenant:
            if not mpesa_available:
                response = "END M-Pesa service is not available. Please contact support."
            else:
                try:
                    # Format phone number for M-Pesa
                    formatted_phone = mpesa_service.format_phone_number(phone_number)
                    print(f"Formatted phone: {formatted_phone}")
                    
                    # Send STK push
                    print(f"Sending STK push for amount: {tenant['rent_due']}")
                    stk_response = mpesa_service.send_stk_push(
                        phone=formatted_phone,
                        amount=tenant['rent_due'],
                        account_ref=f"RENT_{tenant['house_number']}",
                        description=f"Rent {tenant['estate']}"
                    )
                    
                    print(f"STK push response: {stk_response}")
                    
                    if stk_response.get('ResponseCode') == '0':
                        response = "CON M-Pesa STK Push Sent!\n\n"
                        response += "Check your phone for M-Pesa prompt\n"
                        response += "Enter PIN to complete payment\n\n"
                        response += "1. Payment completed\n"
                        response += "#. Back to payment methods\n"
                        response += "0. Exit"
                    else:
                        error_msg = stk_response.get('errorMessage', 'Unknown error')
                        response = f"END STK push failed: {error_msg}"
                        
                except Exception as e:
                    print(f"STK push error: {str(e)}")
                    response = f"END Payment error: {str(e)}"
        else:
            response = "END Session expired. Please dial again."

    elif text == '2*1*2':
        # Airtel Money payment (placeholder for future implementation)
        response = "CON Airtel Money Payment\n\n"
        response += "Airtel Money integration coming soon!\n\n"
        response += "1. Back to payment methods\n"
        response += "#. Back to payment menu\n"
        response += "0. Exit"

    elif text == '2*1*3':
        # Back to payment confirmation
        tenant = TENANT_DB.get(phone_number, None)
        if tenant:
            response = f"CON Pay Full Rent\n\n"
            response += f"Amount to pay: KES {tenant['rent_due']:,}\n\n"
            response += "1. Confirm payment\n"
            response += "2. Back to main menu\n"
            response += "0. Exit"
        else:
            response = "END Session expired. Please dial again."

    elif text == '2*1*1*1':
        # M-Pesa payment completed
        response = "END Payment successful! You will receive an SMS confirmation. Thank you for using RentPay USSD."

    elif text == '2*1*2*1':
        # Back to payment methods from Airtel Money
        response = "CON Payment Method:\n\n"
        response += "1. M-Pesa\n"
        response += "2. Airtel Money\n"
        response += "#. Back to payment menu\n"
        response += "0. Exit"

    # Handle # for going back
    elif text.endswith('#'):
        # Remove the # and go back one level
        previous_text = text[:-1]
        if previous_text == '':
            # If just #, go to main menu
            tenant = TENANT_DB.get(phone_number, None)
            if tenant:
                response = f"CON Welcome, {tenant['name']}. {tenant['house_number']}, {tenant['estate']}\n\n"
                response += "1. Check dues\n"
                response += "2. Pay rent\n"
                response += "0. Exit"
            else:
                response = "END Session expired. Please dial again."
        elif previous_text == '2*1':
            # Back from payment methods to payment confirmation
            tenant = TENANT_DB.get(phone_number, None)
            if tenant:
                response = f"CON Pay Full Rent\n\n"
                response += f"Amount to pay: KES {tenant['rent_due']:,}\n\n"
                response += "1. Confirm payment\n"
                response += "2. Back to main menu\n"
                response += "0. Exit"
            else:
                response = "END Session expired. Please dial again."
        elif previous_text == '2':
            # Back from payment confirmation to main menu
            tenant = TENANT_DB.get(phone_number, None)
            if tenant:
                response = f"CON Welcome, {tenant['name']}. {tenant['house_number']}, {tenant['estate']}\n\n"
                response += "1. Check dues\n"
                response += "2. Pay rent\n"
                response += "0. Exit"
            else:
                response = "END Session expired. Please dial again."
        elif previous_text == '1':
            # Back from check dues to main menu
            tenant = TENANT_DB.get(phone_number, None)
            if tenant:
                response = f"CON Welcome, {tenant['name']}. {tenant['house_number']}, {tenant['estate']}\n\n"
                response += "1. Check dues\n"
                response += "2. Pay rent\n"
                response += "0. Exit"
            else:
                response = "END Session expired. Please dial again."
        else:
            # For other levels, try to go back one step
            response = "END Invalid back navigation. Please dial again."

    else:
        # Handle invalid choices
        response = "END Invalid choice. Please dial again."

    # Send the response back to the API
    return response

@app.route("/mpesa/callback", methods=['POST'])
def mpesa_callback():
    """Handle M-Pesa payment callbacks"""
    try:
        callback_data = request.get_json()
        
        # Log the callback data
        print(f"M-Pesa Callback: {callback_data}")
        
        # Process the callback data
        # In production, you would:
        # 1. Verify the callback signature
        # 2. Update payment status in database
        # 3. Send confirmation SMS to tenant
        # 4. Update rent due amount
        
        return jsonify({"status": "success", "message": "Callback received"}), 200
        
    except Exception as e:
        print(f"Callback error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/debug/mpesa", methods=['GET'])
def debug_mpesa():
    """Debug endpoint to check M-Pesa service status"""
    try:
        config_status = {
            "consumer_key": "Set" if os.getenv('MPESA_CONSUMER_KEY') else "Not set",
            "consumer_secret": "Set" if os.getenv('MPESA_CONSUMER_SECRET') else "Not set",
            "shortcode": "Set" if os.getenv('MPESA_SHORTCODE') else "Not set",
            "passkey": "Set" if os.getenv('MPESA_PASSKEY') else "Not set",
            "sandbox": os.getenv('MPESA_SANDBOX', 'true'),
            "callback_url": os.getenv('MPESA_CALLBACK_URL', 'Not set')
        }
        
        return jsonify({
            "mpesa_service_available": mpesa_available,
            "config_status": config_status,
            "env_file_exists": os.path.exists('.env')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/test/mpesa", methods=['GET'])
def test_mpesa():
    """Test endpoint to validate M-Pesa configuration and test STK push"""
    try:
        if not mpesa_available:
            return jsonify({"error": "M-Pesa service not available"}), 500
        
        # Test phone number formatting
        test_phone = "+254792138852"
        formatted_phone = mpesa_service.format_phone_number(test_phone)
        
        # Test password generation
        password = mpesa_service.generate_password("174379", "test_passkey")
        
        # Test access token generation
        try:
            access_token = mpesa_service.generate_access_token(
                mpesa_service.config.MPESA_CONSUMER_KEY,
                mpesa_service.config.MPESA_CONSUMER_SECRET,
                'test'
            )
            token_status = "Generated successfully"
        except Exception as e:
            token_status = f"Failed: {str(e)}"
        
        return jsonify({
            "mpesa_service_available": mpesa_available,
            "phone_formatting": {
                "original": test_phone,
                "formatted": formatted_phone
            },
            "password_generation": {
                "sample_password": password[:20] + "..."
            },
            "access_token": token_status,
            "config": {
                "shortcode": mpesa_service.config.MPESA_SHORTCODE,
                "sandbox": mpesa_service.config.MPESA_SANDBOX,
                "base_url": mpesa_service.config.MPESA_BASE_URL,
                "callback_url": mpesa_service.config.MPESA_CALLBACK_URL
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)