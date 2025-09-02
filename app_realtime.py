#!/usr/bin/env python3
"""
Lucky Draw Web Application with Real-Time Payment Integration
A Flask-based web application for managing lucky draw ticket bookings with Razorpay integration
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_socketio import SocketIO, emit
import pandas as pd
import os
import json
from datetime import datetime
import shutil
# import razorpay  # Commented out due to environment issues
import uuid

app = Flask(__name__)
app.secret_key = SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuration
TICKET_PRICE = 5
UPI_ID = "9353539771@pthdfc"
TOTAL_TICKETS = 500

# Razorpay Configuration (Replace with your actual keys)
RAZORPAY_KEY_ID = "rzp_test_RCR5h6SGPZzgsE"  # Your Key ID
RAZORPAY_KEY_SECRET = "ymjnVfFTax8cruQAuHY6a2Kl"    # Your Key Secret

# Production Configuration
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
DEBUG = os.environ.get('FLASK_ENV') != 'production'

# Initialize Razorpay client (commented out due to environment issues)
# razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# File paths
EXCEL_FILE = "data/bookings.xlsx"
TICKETS_FILE = "data/tickets.json"

# Global dictionaries for payment management
VALID_TRANSACTIONS = {
    "524472913877": {"amount": 10, "verified": True}  # Your test transaction
}

# Real-time payment tracking
PENDING_PAYMENTS = {}  # Store pending payments
RECENT_PAYMENTS = {}   # Store recently received payments
PAYMENT_ORDERS = {}    # Store Razorpay orders

def ensure_data_directory():
    """Ensure data directory exists"""
    os.makedirs("data", exist_ok=True)

def initialize_excel():
    """Initialize Excel file with headers if it doesn't exist"""
    if not os.path.exists(EXCEL_FILE):
        df = pd.DataFrame(columns=[
            'Name', 'Mobile', 'Tickets', 'Total_Amount', 
            'Payment_Status', 'Transaction_Ref', 'Booking_Date', 'Razorpay_Order_ID'
        ])
        df.to_excel(EXCEL_FILE, index=False)

def initialize_tickets():
    """Initialize tickets JSON file"""
    if not os.path.exists(TICKETS_FILE):
        tickets = {}
        for i in range(1, TOTAL_TICKETS + 1):
            ticket_key = f"{i:04d}"
            tickets[ticket_key] = {"available": True}
        
        with open(TICKETS_FILE, 'w') as f:
            json.dump(tickets, f, indent=2)

def load_tickets():
    """Load ticket availability from JSON file"""
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_tickets(tickets):
    """Save ticket availability to JSON file"""
    with open(TICKETS_FILE, 'w') as f:
        json.dump(tickets, f, indent=2)

def update_ticket_availability(selected_tickets):
    """Update ticket availability after booking"""
    tickets = load_tickets()
    for ticket in selected_tickets:
        if ticket in tickets:
            tickets[ticket]["available"] = False
    save_tickets(tickets)

def create_razorpay_order(amount, user_data):
    """Create a Razorpay order for payment"""
    try:
        # Generate a simple order ID for testing
        order_id = f"order_{uuid.uuid4().hex[:16]}"
        
        # Create order data
        order_data = {
            'id': order_id,
            'amount': amount * 100,  # Razorpay expects amount in paise
            'currency': 'INR',
            'receipt': f"lucky_draw_{uuid.uuid4().hex[:8]}",
            'status': 'created',
            'created_at': int(datetime.now().timestamp())
        }
        
        # Store order details
        PAYMENT_ORDERS[order_id] = {
            'user_data': user_data,
            'amount': amount,
            'status': 'created',
            'created_at': datetime.now().isoformat()
        }
        
        print(f"💰 Created test order: {order_id} for ₹{amount}")
        return order_data
        
    except Exception as e:
        print(f"❌ Error creating order: {e}")
        return None

def verify_razorpay_payment(payment_id, order_id, signature):
    """Verify Razorpay payment signature (simplified for testing)"""
    try:
        # For testing, we'll just check if the order exists
        if order_id in PAYMENT_ORDERS:
            return True
        return False
    except Exception as e:
        print(f"❌ Payment verification failed: {e}")
        return False

def add_valid_transaction(transaction_id, amount):
    """Add a valid transaction to the database"""
    VALID_TRANSACTIONS[transaction_id] = {
        "amount": amount,
        "verified": True,
        "timestamp": datetime.now().isoformat()
    }

def verify_transaction(transaction_id, expected_amount):
    """Verify if a transaction ID is valid"""
    if transaction_id in VALID_TRANSACTIONS:
        transaction = VALID_TRANSACTIONS[transaction_id]
        return transaction["verified"] and transaction["amount"] == expected_amount
    return False

def add_pending_payment(session_id, user_data):
    """Add a payment to pending payments for automatic verification"""
    PENDING_PAYMENTS[session_id] = {
        'user_name': user_data['name'],
        'user_mobile': user_data['mobile'],
        'amount': user_data['total_amount'],
        'tickets': user_data['tickets'],
        'timestamp': datetime.now(),
        'status': 'pending'
    }
    print(f"⏳ Added pending payment: {user_data['name']} - ₹{user_data['total_amount']}")

def check_automatic_payments():
    """Check for automatic payment verification"""
    current_time = datetime.now()
    
    for session_id, payment in PENDING_PAYMENTS.items():
        if payment['status'] != 'pending':
            continue
            
        # Look for matching payment amount in recent payments
        amount = payment['amount']
        
        # Check if we have a recent payment matching this amount
        if amount in RECENT_PAYMENTS:
            # Auto-approve the payment
            timestamp = int(current_time.timestamp())
            transaction_id = str(timestamp).zfill(12)  # Ensure exactly 12 digits
            add_valid_transaction(transaction_id, amount)
            
            payment['status'] = 'auto_verified'
            payment['transaction_id'] = transaction_id
            payment['verified_at'] = current_time.strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"✅ Auto-verified payment: {payment['user_name']} - ₹{amount} - ID: {transaction_id}")
            
            # Remove from recent payments
            del RECENT_PAYMENTS[amount]
            
            return session_id, transaction_id
    
    return None, None

def add_received_payment(amount, actual_transaction_id=None):
    """Add a received payment to the system"""
    current_time = datetime.now()
    
    if actual_transaction_id:
        # Use provided transaction ID
        transaction_id = actual_transaction_id
        add_valid_transaction(transaction_id, amount)
    else:
        # Generate new transaction ID
        timestamp = int(current_time.timestamp())
        transaction_id = str(timestamp).zfill(12)
        add_valid_transaction(transaction_id, amount)
    
    # Add to recent payments for auto-verification
    RECENT_PAYMENTS[amount] = {
        'transaction_id': transaction_id,
        'received_at': current_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    print(f"💰 Payment received: ₹{amount} - ID: {transaction_id}")
    
    # Check for automatic verification
    session_id, verified_transaction_id = check_automatic_payments()
    
    if session_id:
        return f"Auto-verified payment for session {session_id}"
    else:
        return f"Payment added to recent payments. Waiting for matching pending payment."

def get_statistics():
    """Get statistics for admin dashboard"""
    try:
        # Load bookings
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            total_bookings = len(df)
            total_revenue = df['Total_Amount'].sum() if 'Total_Amount' in df.columns else 0
        else:
            total_bookings = 0
            total_revenue = 0
        
        # Load tickets
        tickets = load_tickets()
        booked_tickets = sum(1 for ticket in tickets.values() if not ticket.get('available', True))
        
        return {
            'total_tickets': TOTAL_TICKETS,
            'booked_tickets': booked_tickets,
            'total_bookings': total_bookings,
            'total_revenue': total_revenue
        }
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return {
            'total_tickets': TOTAL_TICKETS,
            'booked_tickets': 0,
            'total_bookings': 0,
            'total_revenue': 0
        }

# WebSocket Events
@socketio.on('connect')
def handle_connect():
    print(f"🔌 Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"🔌 Client disconnected: {request.sid}")

@socketio.on('join_payment_session')
def handle_join_payment_session(data):
    """Join a payment session for real-time updates"""
    session_id = data.get('session_id')
    if session_id:
        print(f"👤 User joined payment session: {session_id}")
        emit('payment_session_joined', {'session_id': session_id})

@socketio.on('payment_completed')
def handle_payment_completed(data):
    """Handle payment completion notification"""
    order_id = data.get('order_id')
    payment_id = data.get('payment_id')
    
    if order_id and order_id in PAYMENT_ORDERS:
        # Update order status
        PAYMENT_ORDERS[order_id]['status'] = 'completed'
        PAYMENT_ORDERS[order_id]['payment_id'] = payment_id
        PAYMENT_ORDERS[order_id]['completed_at'] = datetime.now().isoformat()
        
        # Get user data
        user_data = PAYMENT_ORDERS[order_id]['user_data']
        amount = PAYMENT_ORDERS[order_id]['amount']
        
        # Complete booking
        complete_booking_with_razorpay(order_id, payment_id, user_data, amount)
        
        # Notify all clients about payment completion
        socketio.emit('payment_success', {
            'order_id': order_id,
            'user_name': user_data['name'],
            'amount': amount,
            'tickets': user_data['tickets']
        })
        
        print(f"✅ Payment completed: {user_data['name']} - ₹{amount}")

def complete_booking_with_razorpay(order_id, payment_id, user_data, amount):
    """Complete booking with Razorpay payment details"""
    try:
        ensure_data_directory()
        initialize_excel()
        
        # Prepare booking data
        booking_data = {
            'Name': user_data['name'],
            'Mobile': user_data['mobile'],
            'Tickets': ', '.join(user_data['tickets']),
            'Total_Amount': amount,
            'Payment_Status': 'Paid',
            'Transaction_Ref': payment_id,
            'Booking_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Razorpay_Order_ID': order_id
        }
        
        # Save to Excel
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([booking_data])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        
        # Update ticket availability
        update_ticket_availability(user_data['tickets'])
        
        print(f"✅ Booking completed: {user_data['name']} - Order: {order_id}")
        
    except Exception as e:
        print(f"❌ Error completing booking: {e}")

@app.route('/test_razorpay')
def test_razorpay():
    """Test Razorpay payment window"""
    return send_file('test_razorpay.html')

@app.route('/')
def index():
    """Home page with user registration form"""
    return render_template('index.html')

@app.route('/submit_user', methods=['POST'])
def submit_user():
    """Handle user registration and redirect to ticket selection"""
    name = request.form.get('name')
    mobile = request.form.get('mobile')
    
    if not name or not mobile:
        flash('Please fill in all fields', 'error')
        return redirect(url_for('index'))
    
    if len(mobile) != 10 or not mobile.isdigit():
        flash('Please enter a valid 10-digit mobile number', 'error')
        return redirect(url_for('index'))
    
    # Store user data in session
    session['user_name'] = name
    session['user_mobile'] = mobile
    
    return redirect(url_for('select_tickets'))

@app.route('/tickets')
def select_tickets():
    """Ticket selection page"""
    if 'user_name' not in session:
        return redirect(url_for('index'))
    
    tickets = load_tickets()
    return render_template('tickets.html', 
                         tickets=tickets, 
                         ticket_price=TICKET_PRICE,
                         user_name=session['user_name'])

@app.route('/process_ticket_selection', methods=['POST'])
def process_ticket_selection():
    """Process ticket selection and redirect to payment"""
    if 'user_name' not in session:
        return redirect(url_for('index'))
    
    selected_tickets = request.form.getlist('tickets')
    
    if not selected_tickets:
        flash('Please select at least one ticket', 'error')
        return redirect(url_for('select_tickets'))
    
    # Check if tickets are still available
    tickets = load_tickets()
    unavailable_tickets = []
    
    for ticket in selected_tickets:
        if ticket not in tickets or not tickets[ticket].get('available', True):
            unavailable_tickets.append(ticket)
    
    if unavailable_tickets:
        flash(f'Tickets {", ".join(unavailable_tickets)} are no longer available', 'error')
        return redirect(url_for('select_tickets'))
    
    # Calculate total amount
    total_amount = len(selected_tickets) * TICKET_PRICE
    
    # Store in session
    session['selected_tickets'] = selected_tickets
    session['total_amount'] = total_amount
    
    return redirect(url_for('payment'))

@app.route('/payment')
def payment():
    """Payment page with real-time payment integration"""
    if 'user_name' not in session or 'selected_tickets' not in session:
        return redirect(url_for('index'))
    
    user_data = {
        'name': session['user_name'],
        'mobile': session['user_mobile'],
        'tickets': session['selected_tickets'],
        'ticket_count': len(session['selected_tickets']),
        'total_amount': session['total_amount'],
        'upi_id': UPI_ID
    }
    
    # Create Razorpay order
    order = create_razorpay_order(user_data['total_amount'], user_data)
    
    if order:
        session['razorpay_order_id'] = order['id']
        session['payment_session_id'] = order['id']
        
        return render_template('payment_realtime.html', 
                             user_data=user_data, 
                             order=order,
                             razorpay_key_id=RAZORPAY_KEY_ID)
    else:
        flash('Unable to create payment order. Please try again.', 'error')
        return redirect(url_for('select_tickets'))

@app.route('/payment_manual')
def payment_manual():
    """Manual payment page with transaction ID entry"""
    if 'user_name' not in session or 'selected_tickets' not in session:
        return redirect(url_for('index'))
    
    user_data = {
        'name': session['user_name'],
        'mobile': session['user_mobile'],
        'tickets': session['selected_tickets'],
        'ticket_count': len(session['selected_tickets']),
        'total_amount': session['total_amount'],
        'upi_id': UPI_ID
    }
    
    return render_template('payment.html', user_data=user_data)

@app.route('/verify_payment', methods=['POST'])
def verify_payment():
    """Verify payment and complete booking (fallback method)"""
    if 'user_name' not in session or 'selected_tickets' not in session:
        return redirect(url_for('index'))
    
    transaction_ref = request.form.get('transaction_ref', '').strip()
    
    if not transaction_ref:
        flash('Please enter the transaction reference number', 'error')
        return redirect(url_for('payment'))
    
    if len(transaction_ref) != 12 or not transaction_ref.isdigit():
        flash('Transaction ID must be exactly 12 digits', 'error')
        return redirect(url_for('payment'))
    
    # Verify transaction
    expected_amount = session['total_amount']
    if verify_transaction(transaction_ref, expected_amount):
        # Payment verified, complete booking
        return complete_booking(transaction_ref)
    else:
        flash('Invalid transaction ID or amount mismatch. Please check and try again.', 'error')
        return redirect(url_for('payment'))

def complete_booking(transaction_ref):
    """Complete the booking process"""
    try:
        ensure_data_directory()
        initialize_excel()
        
        # Prepare booking data
        booking_data = {
            'Name': session['user_name'],
            'Mobile': session['user_mobile'],
            'Tickets': ', '.join(session['selected_tickets']),
            'Total_Amount': session['total_amount'],
            'Payment_Status': 'Paid',
            'Transaction_Ref': transaction_ref,
            'Booking_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save to Excel
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, pd.DataFrame([booking_data])], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        
        # Update ticket availability
        update_ticket_availability(session['selected_tickets'])
        
        # Prepare user data for success page
        user_data = {
            'name': session['user_name'],
            'mobile': session['user_mobile'],
            'tickets': session['selected_tickets'],
            'total_amount': session['total_amount'],
            'transaction_ref': transaction_ref
        }
        
        # Clear session
        session.clear()
        
        return render_template('success.html', user_data=user_data)
        
    except Exception as e:
        print(f"Error completing booking: {e}")
        flash('An error occurred while completing your booking. Please try again.', 'error')
        return redirect(url_for('payment'))

# Razorpay Webhook endpoint
@app.route('/razorpay_webhook', methods=['POST'])
def razorpay_webhook():
    """Handle Razorpay webhook for payment confirmation"""
    try:
        # Verify webhook signature
        webhook_signature = request.headers.get('X-Razorpay-Signature')
        webhook_body = request.get_data()
        
        # Verify webhook (you should implement proper signature verification)
        # razorpay_client.utility.verify_webhook_signature(webhook_body, webhook_signature, webhook_secret)
        
        # Parse webhook data
        webhook_data = request.get_json()
        event = webhook_data.get('event')
        
        if event == 'payment.captured':
            payment_data = webhook_data.get('payload', {}).get('payment', {})
            order_id = payment_data.get('order_id')
            payment_id = payment_data.get('id')
            amount = payment_data.get('amount') / 100  # Convert from paise to rupees
            
            if order_id and order_id in PAYMENT_ORDERS:
                # Update order status
                PAYMENT_ORDERS[order_id]['status'] = 'completed'
                PAYMENT_ORDERS[order_id]['payment_id'] = payment_id
                PAYMENT_ORDERS[order_id]['completed_at'] = datetime.now().isoformat()
                
                # Get user data
                user_data = PAYMENT_ORDERS[order_id]['user_data']
                
                # Complete booking
                complete_booking_with_razorpay(order_id, payment_id, user_data, amount)
                
                # Notify all clients about payment completion
                socketio.emit('payment_success', {
                    'order_id': order_id,
                    'user_name': user_data['name'],
                    'amount': amount,
                    'tickets': user_data['tickets']
                })
                
                print(f"✅ Webhook: Payment completed for {user_data['name']} - ₹{amount}")
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return jsonify({'status': 'error'}), 500

# Admin Routes
@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    stats = get_statistics()
    pending_count = len([p for p in PENDING_PAYMENTS.values() if p['status'] == 'pending'])
    return render_template('admin_dashboard.html', stats=stats, pending_count=pending_count)

@app.route('/admin/reset_data')
def admin_reset_data():
    """Reset all data"""
    try:
        # Remove Excel file
        if os.path.exists(EXCEL_FILE):
            os.remove(EXCEL_FILE)
        
        # Remove tickets file
        if os.path.exists(TICKETS_FILE):
            os.remove(TICKETS_FILE)
        
        # Clear global variables
        PENDING_PAYMENTS.clear()
        RECENT_PAYMENTS.clear()
        VALID_TRANSACTIONS.clear()
        PAYMENT_ORDERS.clear()
        
        # Reinitialize
        initialize_excel()
        initialize_tickets()
        
        flash('All data has been reset successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
        
    except Exception as e:
        flash(f'Error resetting data: {e}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/export_data')
def admin_export_data():
    """Export data to Excel"""
    try:
        if os.path.exists(EXCEL_FILE):
            return send_file(EXCEL_FILE, as_attachment=True, download_name='lucky_draw_bookings.xlsx')
        else:
            flash('No data to export', 'error')
            return redirect(url_for('admin_dashboard'))
    except Exception as e:
        flash(f'Error exporting data: {e}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/view_bookings')
def admin_view_bookings():
    """View all bookings"""
    try:
        if os.path.exists(EXCEL_FILE):
            df = pd.read_excel(EXCEL_FILE)
            bookings = df.to_dict('records')
        else:
            bookings = []
        
        return render_template('admin_bookings.html', bookings=bookings)
    except Exception as e:
        flash(f'Error loading bookings: {e}', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/pending_payments')
def admin_pending_payments():
    """View pending payments"""
    if not PENDING_PAYMENTS:
        return "No pending payments"
    
    result = "<h2>📋 Pending Payments</h2><br>"
    for session_id, payment in PENDING_PAYMENTS.items():
        result += f"""
        <div style='border: 1px solid #ccc; padding: 10px; margin: 10px;'>
            <strong>Session ID:</strong> <code>{session_id}</code> (12 digits)<br>
            <strong>User:</strong> {payment['user_name']} ({payment['user_mobile']})<br>
            <strong>Amount:</strong> ₹{payment['amount']}<br>
            <strong>Tickets:</strong> {', '.join(payment['tickets'])}<br>
            <strong>Status:</strong> {payment['status']}<br>
            <strong>Time:</strong> {payment['timestamp']}<br>
            <a href='/admin/payment_received/{payment['amount']}'>Mark as Received</a>
        </div>
        """
    return result

@app.route('/admin/recent_payments')
def admin_recent_payments():
    """View recent payments"""
    if not RECENT_PAYMENTS:
        return "No recent payments"
    
    result = "<h2>💰 Recent Payments</h2><br>"
    for amount, payment in RECENT_PAYMENTS.items():
        result += f"""
        <div style='border: 1px solid #ccc; padding: 10px; margin: 10px;'>
            <strong>Amount:</strong> ₹{amount}<br>
            <strong>Received At:</strong> {payment['received_at']}<br>
            <strong>Transaction ID:</strong> {payment['transaction_id']}<br>
        </div>
        """
    return result

@app.route('/admin/payment_received/<int:amount>')
@app.route('/admin/payment_received/<int:amount>/<transaction_id>')
def mark_payment_received(amount, transaction_id=None):
    """Admin route: Mark a payment as received"""
    result = add_received_payment(amount, transaction_id)
    return f"💰 Payment of ₹{amount} marked as received. {result}"

@app.route('/admin/check_payments')
def admin_check_payments():
    """Admin route: Manually trigger payment verification check"""
    session_id, transaction_id = check_automatic_payments()
    if session_id:
        return f"✅ Auto-verified payment for session {session_id} with transaction ID {transaction_id}"
    else:
        return "⏳ No payments to auto-verify at this time"

@app.route('/admin/add_manual_payment', methods=['POST'])
def admin_add_manual_payment():
    """Add manual payment entry"""
    try:
        amount = int(request.form.get('amount'))
        transaction_id = request.form.get('transaction_id', '').strip()
        
        if amount < 5:
            flash('Amount must be at least ₹5', 'error')
            return redirect(url_for('admin_dashboard'))
        
        if transaction_id and (len(transaction_id) != 12 or not transaction_id.isdigit()):
            flash('Transaction ID must be exactly 12 digits', 'error')
            return redirect(url_for('admin_dashboard'))
        
        result = add_received_payment(amount, transaction_id if transaction_id else None)
        flash(f'Payment added successfully! {result}', 'success')
        
    except Exception as e:
        flash(f'Error adding payment: {e}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/generate_qr')
def admin_generate_qr():
    """Generate new QR code"""
    try:
        import subprocess
        subprocess.run(['python', 'generate_website_qr.py'], check=True)
        flash('QR code generated successfully!', 'success')
    except Exception as e:
        flash(f'Error generating QR code: {e}', 'error')
    
    return redirect(url_for('admin_dashboard'))

# Real-time payment verification endpoint
@app.route('/api/check_payment/<session_id>')
def api_check_payment(session_id):
    """API endpoint for real-time payment checking"""
    if session_id in PENDING_PAYMENTS:
        payment = PENDING_PAYMENTS[session_id]
        if payment['status'] == 'auto_verified':
            return jsonify({
                'status': 'verified',
                'transaction_id': payment.get('transaction_id'),
                'message': 'Payment verified successfully!'
            })
        elif payment['status'] == 'pending':
            return jsonify({
                'status': 'pending',
                'message': 'Payment pending verification...'
            })
    
    return jsonify({
        'status': 'not_found',
        'message': 'Payment session not found'
    })

if __name__ == '__main__':
    ensure_data_directory()
    initialize_excel()
    initialize_tickets()
    print("🎯 Lucky Draw Application with Real-Time Payments Started!")
    print("🌐 Website: http://localhost:5000")
    print("🔧 Admin Panel: http://localhost:5000/admin")
    print("📱 QR Code: Run 'python generate_website_qr.py' to generate")
    print("💳 Razorpay Integration: Configure your API keys in the code")
    
    # Production vs Development
    if DEBUG:
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    else:
        # For production, use the port provided by the hosting platform
        port = int(os.environ.get('PORT', 5000))
        socketio.run(app, host='0.0.0.0', port=port)
