from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from sms_service import SMSService
from datetime import datetime, timedelta
import json

app = Flask(__name__)

# Add custom Jinja2 filter for number formatting
@app.template_filter('number_format')
def number_format(value):
    """Format numbers with comma separators"""
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return str(value)

# Initialize SMS service
sms_service = SMSService()

# Mock tenant database - in production, this would connect to a real database
TENANT_DB = {
    "+254792138852": {
        "name": "John",
        "house_number": "HSe no. 4",
        "estate": "Killimani estate",
        "rent_due": 25000,
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

# USSD code for the rent payment system
USSD_CODE = "*384*11897#"

# HTML template for the landlord dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RentPay - Landlord Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.1em; opacity: 0.9; }
        
        .dashboard-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }
        .card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .card h3 { color: #2c3e50; margin-bottom: 20px; font-size: 1.4em; }
        
        .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .stat-number { font-size: 2.5em; font-weight: bold; color: #3498db; }
        .stat-label { color: #7f8c8d; margin-top: 5px; }
        
        .form-group { margin-bottom: 20px; }
        .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #2c3e50; }
        .form-group input, .form-group select, .form-group textarea { 
            width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; 
            transition: border-color 0.3s; }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus { 
            outline: none; border-color: #3498db; }
        
        .btn { background: #3498db; color: white; padding: 12px 25px; border: none; border-radius: 8px; 
               font-size: 16px; cursor: pointer; transition: background 0.3s; }
        .btn:hover { background: #2980b9; }
        .btn-success { background: #27ae60; }
        .btn-success:hover { background: #229954; }
        .btn-danger { background: #e74c3c; }
        .btn-danger:hover { background: #c0392b; }
        
        .tenant-list { max-height: 400px; overflow-y: auto; }
        .tenant-item { 
            display: flex; justify-content: space-between; align-items: center; 
            padding: 15px; border-bottom: 1px solid #ecf0f1; 
        }
        .tenant-info h4 { color: #2c3e50; margin-bottom: 5px; }
        .tenant-info p { color: #7f8c8d; font-size: 0.9em; }
        .tenant-actions { display: flex; gap: 10px; }
        
        .alert { padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .alert-info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        
        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; 
                background-color: rgba(0,0,0,0.5); }
        .modal-content { background-color: white; margin: 5% auto; padding: 30px; border-radius: 10px; 
                         width: 80%; max-width: 600px; }
        .close { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
        .close:hover { color: #000; }
        
        @media (max-width: 768px) {
            .dashboard-grid { grid-template-columns: 1fr; }
            .stats { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 RentPay Landlord Dashboard</h1>
            <p>Manage your properties and send rent invoices to tenants</p>
        </div>
        
        {% if message %}
        <div class="alert alert-{{ message_type }}">
            {{ message }}
        </div>
        {% endif %}
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ total_tenants }}</div>
                <div class="stat-label">Total Tenants</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">KES {{ total_rent_due | number_format }}</div>
                <div class="stat-label">Total Rent Due</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ ussd_code }}</div>
                <div class="stat-label">USSD Code</div>
            </div>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h3>📱 Send Rent Invoice</h3>
                <form method="POST" action="/send-invoice">
                    <div class="form-group">
                        <label for="tenant_phone">Select Tenant:</label>
                        <select name="tenant_phone" id="tenant_phone" required>
                            <option value="">Choose a tenant...</option>
                            {% for phone, tenant in tenants.items() %}
                            <option value="{{ phone }}">{{ tenant.name }} - {{ tenant.house_number }}, {{ tenant.estate }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="rent_amount">Rent Amount (KES):</label>
                        <input type="number" name="rent_amount" id="rent_amount" required min="1" 
                               placeholder="Enter rent amount">
                    </div>
                    
                    <div class="form-group">
                        <label for="due_date">Due Date:</label>
                        <input type="date" name="due_date" id="due_date" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="custom_message">Custom Message (Optional):</label>
                        <textarea name="custom_message" id="custom_message" rows="3" 
                                  placeholder="Add any additional message..."></textarea>
                    </div>
                    
                    <button type="submit" class="btn btn-success">📤 Send Invoice SMS</button>
                </form>
            </div>
            
            <div class="card">
                <h3>📋 Tenant List</h3>
                <div class="tenant-list">
                    {% for phone, tenant in tenants.items() %}
                    <div class="tenant-item">
                        <div class="tenant-info">
                            <h4>{{ tenant.name }}</h4>
                            <p>{{ tenant.house_number }}, {{ tenant.estate }}</p>
                            <p>Rent: KES {{ tenant.rent_due | number_format }}</p>
                        </div>
                        <div class="tenant-actions">
                            <button class="btn" onclick="sendQuickInvoice('{{ phone }}', '{{ tenant.name }}', {{ tenant.rent_due }})">
                                📱 Quick Invoice
                            </button>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>📤 Bulk Invoice Sender</h3>
            <form method="POST" action="/send-bulk-invoices">
                <div class="form-group">
                    <label>Select Tenants for Bulk Invoice:</label>
                    <div style="max-height: 200px; overflow-y: auto; border: 1px solid #e0e0e0; padding: 15px; border-radius: 8px;">
                        {% for phone, tenant in tenants.items() %}
                        <label style="display: block; margin-bottom: 10px;">
                            <input type="checkbox" name="selected_tenants" value="{{ phone }}" style="margin-right: 10px;">
                            {{ tenant.name }} - {{ tenant.house_number }}, {{ tenant.estate }} (KES {{ tenant.rent_due | number_format }})
                        </label>
                        {% endfor %}
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="bulk_rent_amount">Standard Rent Amount (KES):</label>
                    <input type="number" name="bulk_rent_amount" id="bulk_rent_amount" required min="1" 
                           placeholder="Enter standard rent amount for all selected tenants">
                </div>
                
                <div class="form-group">
                    <label for="bulk_due_date">Due Date:</label>
                    <input type="date" name="bulk_due_date" id="bulk_due_date" required>
                </div>
                
                <button type="submit" class="btn btn-success">📤 Send Bulk Invoices</button>
            </form>
        </div>
    </div>
    
    <!-- Quick Invoice Modal -->
    <div id="quickInvoiceModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h3>📱 Quick Invoice</h3>
            <form id="quickInvoiceForm" method="POST" action="/send-invoice">
                <input type="hidden" name="tenant_phone" id="modal_tenant_phone">
                <div class="form-group">
                    <label for="modal_tenant_name">Tenant:</label>
                    <input type="text" id="modal_tenant_name" readonly>
                </div>
                <div class="form-group">
                    <label for="modal_rent_amount">Rent Amount (KES):</label>
                    <input type="number" name="rent_amount" id="modal_rent_amount" required min="1">
                </div>
                <div class="form-group">
                    <label for="modal_due_date">Due Date:</label>
                    <input type="date" name="due_date" id="modal_due_date" required>
                </div>
                <button type="submit" class="btn btn-success">📤 Send Invoice</button>
            </form>
        </div>
    </div>
    
    <script>
        // Set default due date to next month
        document.addEventListener('DOMContentLoaded', function() {
            const today = new Date();
            const nextMonth = new Date(today.getFullYear(), today.getMonth() + 1, today.getDate());
            const dueDate = nextMonth.toISOString().split('T')[0];
            
            document.getElementById('due_date').value = dueDate;
            document.getElementById('bulk_due_date').value = dueDate;
        });
        
        function sendQuickInvoice(phone, name, currentRent) {
            document.getElementById('modal_tenant_phone').value = phone;
            document.getElementById('modal_tenant_name').value = name;
            document.getElementById('modal_rent_amount').value = currentRent;
            document.getElementById('modal_due_date').value = document.getElementById('due_date').value;
            document.getElementById('quickInvoiceModal').style.display = 'block';
        }
        
        function closeModal() {
            document.getElementById('quickInvoiceModal').style.display = 'none';
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('quickInvoiceModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Landlord dashboard main page"""
    # Calculate totals
    total_tenants = len(TENANT_DB)
    total_rent_due = sum(tenant['rent_due'] for tenant in TENANT_DB.values())
    
    return render_template_string(DASHBOARD_HTML, 
                                tenants=TENANT_DB,
                                total_tenants=total_tenants,
                                total_rent_due=total_rent_due,
                                ussd_code=USSD_CODE)

@app.route('/send-invoice', methods=['POST'])
def send_invoice():
    """Send rent invoice to a single tenant"""
    try:
        tenant_phone = request.form.get('tenant_phone')
        rent_amount = int(request.form.get('rent_amount'))
        due_date = request.form.get('due_date')
        custom_message = request.form.get('custom_message', '')
        
        if not tenant_phone or tenant_phone not in TENANT_DB:
            return redirect('/?message=Invalid tenant selected&message_type=error')
        
        tenant = TENANT_DB[tenant_phone]
        
        # Send SMS invoice
        result = sms_service.send_rent_invoice(
            tenant_phone=tenant_phone,
            tenant_name=tenant['name'],
            house_number=tenant['house_number'],
            estate=tenant['estate'],
            rent_amount=rent_amount,
            due_date=due_date,
            ussd_code=USSD_CODE
        )
        
        if result['success']:
            message = f"Invoice sent successfully to {tenant['name']} (Message ID: {result.get('message_id', 'N/A')})"
            message_type = 'success'
        else:
            message = f"Failed to send invoice: {result.get('error', 'Unknown error')}"
            message_type = 'error'
        
        return redirect(f'/?message={message}&message_type={message_type}')
        
    except Exception as e:
        return redirect(f'/?message=Error: {str(e)}&message_type=error')

@app.route('/send-bulk-invoices', methods=['POST'])
def send_bulk_invoices():
    """Send rent invoices to multiple tenants"""
    try:
        selected_tenants = request.form.getlist('selected_tenants')
        rent_amount = int(request.form.get('bulk_rent_amount'))
        due_date = request.form.get('bulk_due_date')
        
        if not selected_tenants:
            return redirect('/?message=No tenants selected&message_type=error')
        
        # Prepare tenant data for bulk sending
        tenants_data = []
        for phone in selected_tenants:
            if phone in TENANT_DB:
                tenant = TENANT_DB[phone]
                tenants_data.append({
                    'phone': phone,
                    'name': tenant['name'],
                    'house_number': tenant['house_number'],
                    'estate': tenant['estate'],
                    'rent_amount': rent_amount,
                    'due_date': due_date
                })
        
        # Send bulk invoices
        result = sms_service.send_bulk_invoices(tenants_data, USSD_CODE)
        
        message = f"Bulk invoices sent: {result['success_count']} successful, {result['failure_count']} failed"
        message_type = 'success' if result['failure_count'] == 0 else 'info'
        
        return redirect(f'/?message={message}&message_type={message_type}')
        
    except Exception as e:
        return redirect(f'/?message=Error: {str(e)}&message_type=error')

@app.route('/api/tenants')
def api_tenants():
    """API endpoint to get tenant list"""
    return jsonify(TENANT_DB)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
