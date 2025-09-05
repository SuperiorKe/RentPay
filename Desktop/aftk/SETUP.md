# 🚀 Quick Setup Guide

Get RentPay up and running in under 5 minutes!

## ⚡ One-Command Setup

```bash
python quick_setup.py
```

This script will:
- ✅ Install all dependencies
- ✅ Create .env file from template
- ✅ Verify Python version
- ✅ Guide you through next steps

## 📋 Manual Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy environment template
cp env_template.txt .env

# Edit .env with your credentials
# M-Pesa API credentials
# SMS provider credentials
```

### 3. Run Applications

#### USSD Payment System
```bash
python ussd.py
# Runs on http://localhost:5000
```

#### Landlord Dashboard
```bash
python landlord_dashboard.py
# Runs on http://localhost:5001
```

## 🔑 Required Credentials

### M-Pesa (Sandbox)
- Consumer Key
- Consumer Secret
- Shortcode
- Passkey

### SMS Provider (Choose One)
- **Africa's Talking**: API Key, Username, Sender ID
- **Twilio**: Account SID, Auth Token, Phone Number
- **Generic**: No credentials needed (logs to console)

## 🧪 Test the System

1. **Visit Dashboard**: http://localhost:5001
2. **Send Test Invoice**: Use your phone number
3. **Test USSD**: Dial the USSD code from the invoice
4. **Complete Payment**: Follow M-Pesa prompts

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: README.md
- **SMS Guide**: SMS_README.md

---

**Ready to revolutionize rent collection! 🏠💰**
