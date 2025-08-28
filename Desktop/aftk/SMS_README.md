# 📱 RentPay SMS Invoice Service

A comprehensive SMS service for landlords to send rent invoices to tenants with payment instructions.

## ✨ Features

- **📤 Single Invoice Sending** - Send individual rent invoices to specific tenants
- **📤 Bulk Invoice Sending** - Send invoices to multiple tenants at once
- **🏠 Landlord Dashboard** - Beautiful web interface for managing invoices
- **📱 Multiple SMS Providers** - Support for Africa's Talking, Twilio, and generic providers
- **💳 Payment Integration** - Includes USSD code for easy rent payment
- **📊 Real-time Statistics** - View tenant counts and total rent due

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure SMS Service
Copy `sms_env_template.txt` to `.env` and configure your SMS provider:

```bash
# For testing (logs SMS to console)
SMS_PROVIDER=generic

# For production (Africa's Talking)
SMS_PROVIDER=africastalking
SMS_API_KEY=your_api_key
SMS_USERNAME=your_username
SMS_SENDER_ID=RENTPAY

# For production (Twilio)
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number
```

### 3. Run the Landlord Dashboard
```bash
python landlord_dashboard.py
```

The dashboard will run on `http://localhost:5001`

## 🏠 Landlord Dashboard

### **Main Features:**

1. **📊 Statistics Overview**
   - Total tenants count
   - Total rent due amount
   - USSD code display

2. **📱 Send Individual Invoice**
   - Select tenant from dropdown
   - Set rent amount and due date
   - Add custom message (optional)
   - Send invoice via SMS

3. **📋 Tenant Management**
   - View all tenants and their details
   - Quick invoice button for each tenant
   - Current rent amounts

4. **📤 Bulk Invoice Sender**
   - Select multiple tenants
   - Set standard rent amount
   - Send invoices to all selected tenants

### **Dashboard Interface:**

```
🏠 RentPay Landlord Dashboard
├── 📊 Statistics (Tenants, Rent Due, USSD Code)
├── 📱 Send Rent Invoice Form
├── 📋 Tenant List with Quick Actions
└── 📤 Bulk Invoice Sender
```

## 📱 SMS Invoice Format

The SMS sent to tenants includes:

```
RENT INVOICE

Dear [Tenant Name],
House: [House Number]
Estate: [Estate Name]
Rent Due: KES [Amount]
Due Date: [Due Date]

To pay, dial: [USSD Code]

Thank you,
RentPay Team
```

## 🔧 SMS Providers

### **1. Generic/Test Mode**
- **Purpose**: Development and testing
- **Action**: Logs SMS to console
- **Setup**: No configuration needed

### **2. Africa's Talking**
- **Purpose**: Production SMS in East Africa
- **Setup**: Requires API key and username
- **Cost**: Pay-per-SMS

### **3. Twilio**
- **Purpose**: Global SMS service
- **Setup**: Requires account SID and auth token
- **Cost**: Pay-per-SMS

## 📱 USSD Integration

The SMS service integrates with your USSD rent payment system:

- **USSD Code**: `*384*11897#`
- **Payment Flow**: Tenant receives SMS → Dials USSD → Makes payment
- **Seamless Experience**: From invoice to payment completion

## 🧪 Testing

### **Test SMS Sending:**
1. **Start dashboard**: `python landlord_dashboard.py`
2. **Visit**: `http://localhost:5001`
3. **Select tenant** and send test invoice
4. **Check console** for SMS logs (in generic mode)

### **Test with Real SMS:**
1. **Configure SMS provider** in `.env`
2. **Add real phone numbers** to tenant database
3. **Send test invoice** to your phone

## 🚀 Production Deployment

### **Environment Variables:**
- Set `SMS_PROVIDER` to your chosen provider
- Configure API credentials securely
- Use HTTPS for dashboard access

### **Database Integration:**
Replace `TENANT_DB` mock with:
- PostgreSQL/MySQL for tenant data
- User authentication for landlords
- Payment history tracking

### **Additional Features:**
- **SMS Templates** - Customizable invoice formats
- **Scheduled Invoices** - Automatic monthly reminders
- **Payment Confirmations** - SMS notifications for successful payments
- **Analytics Dashboard** - Payment tracking and reporting

## 📞 Support

For technical support or feature requests, contact the development team.

---

**Built with ❤️ for seamless rent collection and tenant communication**
