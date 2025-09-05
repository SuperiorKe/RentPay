# 🏠 RentPay - USSD Rent Payment System

A groundbreaking rent payment solution that combines USSD technology with M-Pesa integration and SMS invoice services for seamless rent collection.

![RentPay](https://img.shields.io/badge/RentPay-USSD%20Payment%20System-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Flask](https://img.shields.io/badge/Flask-2.3+-red)
![M-Pesa](https://img.shields.io/badge/M--Pesa-Integration-orange)

## ✨ Features

### 🎯 **USSD Payment System**
- **Personalized Tenant Experience** - Welcome message with tenant details
- **Real-time Rent Status** - Check dues and payment history
- **M-Pesa STK Push** - Direct mobile money integration
- **Smart Navigation** - Intuitive menu with # for back navigation
- **Payment Callbacks** - Real-time payment confirmation

### 📱 **SMS Invoice Service**
- **Individual Invoice Sending** - Send rent invoices to specific tenants
- **Bulk Invoice Sending** - Send invoices to multiple tenants at once
- **Landlord Dashboard** - Beautiful web interface for managing invoices
- **Multiple SMS Providers** - Support for Africa's Talking, Twilio, and generic
- **Payment Integration** - Includes USSD code for easy rent payment

### 🔧 **Technical Features**
- **Flask Backend** - Scalable and maintainable Python web framework
- **M-Pesa Integration** - Production-ready mobile money integration
- **SMS Service** - Professional invoice delivery system
- **Responsive UI** - Modern dashboard design
- **Error Handling** - Comprehensive error management and logging

## 🚀 Quick Start

### ⚡ One-Command Setup
```bash
git clone https://github.com/SuperiorKe/RentPay.git
cd RentPay
python quick_setup.py
```

### 📋 Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp env_template.txt .env
# Edit .env with your credentials

# 3. Run applications
python ussd.py              # USSD system (port 5000)
python landlord_dashboard.py # Dashboard (port 5001)
```

### 🔑 Required Credentials
- **M-Pesa**: Consumer Key, Secret, Shortcode, Passkey
- **SMS**: Choose Africa's Talking, Twilio, or Generic
- **Detailed setup**: See [SETUP.md](SETUP.md)

## 📱 USSD Flow

### **Main Menu**
```
Welcome, John. HSe no. 4, Killimani estate

1. Check dues
2. Pay rent
0. Exit
```

### **Payment Process**
1. **Select "2. Pay rent"** → Shows payment amount
2. **Confirm payment** → Chooses M-Pesa
3. **STK Push sent** → User gets M-Pesa prompt on phone
4. **Complete payment** → Real-time confirmation

## 🏠 Landlord Dashboard

### **Features**
- **📊 Statistics Overview** - Tenant count, total rent due, USSD code
- **📱 Individual Invoice Sending** - Send to specific tenants
- **📤 Bulk Invoice Sending** - Send to multiple tenants
- **📋 Tenant Management** - View all tenants with quick actions

### **SMS Invoice Format**
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

## 🔧 Configuration

### **M-Pesa Integration**
```bash
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_SHORTCODE=your_shortcode
MPESA_PASSKEY=your_passkey
MPESA_SANDBOX=true
```

### **SMS Service**
```bash
SMS_PROVIDER=africastalking  # or twilio, generic
SMS_API_KEY=your_api_key
SMS_USERNAME=your_username
SMS_SENDER_ID=RENTPAY
```

## 🧪 Testing

### **Test Phone Numbers**
- `+254792138852` → John's account (HSe no. 4)
- `+254715035359` → Kenn's account (HSe no. 12)

### **Test Payment Flow**
1. Dial USSD code: `*384*11897#`
2. Navigate to payment option
3. Select M-Pesa
4. Check phone for STK push
5. Complete payment

## 🏗️ Architecture

### **File Structure**
```
RentPay/
├── 📱 ussd.py                    # Main USSD application
├── 🏠 landlord_dashboard.py      # Landlord dashboard
├── 📱 sms_service.py             # SMS service module
├── ⚙️ config.py                  # M-Pesa configuration
├── 📋 requirements.txt           # Python dependencies
├── 🔧 setup_env.py               # Environment setup script
├── 📖 README.md                  # Project documentation
├── 📱 SMS_README.md              # SMS service documentation
├── 📧 env_template.txt           # Environment variables template
└── 📧 sms_env_template.txt       # SMS configuration template
```

### **Key Components**
- **USSD Application** - Handles mobile payment requests
- **M-Pesa Service** - Manages mobile money integration
- **SMS Service** - Handles invoice delivery
- **Landlord Dashboard** - Web interface for property management

## 🚀 Production Deployment

### **Environment Setup**
- Set `MPESA_SANDBOX=false` for production
- Configure real SMS provider credentials
- Use HTTPS for dashboard access
- Implement proper logging and monitoring

### **Database Integration**
Replace mock databases with:
- PostgreSQL/MySQL for tenant data
- Redis for session management
- MongoDB for payment logs

### **Additional Features**
- **SMS Templates** - Customizable invoice formats
- **Scheduled Invoices** - Automatic monthly reminders
- **Payment Confirmations** - SMS notifications for successful payments
- **Analytics Dashboard** - Payment tracking and reporting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/SuperiorKe/RentPay/issues)
- **Documentation**: Check the [SMS_README.md](SMS_README.md) for detailed setup
- **Email**: Contact the development team

## 🙏 Acknowledgments

- **M-Pesa API** - Mobile money integration
- **Africa's Talking** - SMS service provider
- **Flask** - Web framework
- **Python Community** - Open source libraries

---

**Built with ❤️ for seamless rent collection and tenant communication**

⭐ **Star this repository if you find it helpful!**
