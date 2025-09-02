#!/usr/bin/env python3
"""
Test script to verify Razorpay integration
"""

import razorpay
import json

# Your Razorpay credentials
RAZORPAY_KEY_ID = "rzp_test_RCR5h6SGPZzgsE"
RAZORPAY_KEY_SECRET = "ymjnVfFTax8cruQAuHY6a2Kl"

def test_razorpay_connection():
    """Test Razorpay API connection"""
    try:
        # Initialize Razorpay client
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        
        print("✅ Razorpay client initialized successfully")
        
        # Test creating a small order
        order_data = {
            'amount': 500,  # ₹5 in paise
            'currency': 'INR',
            'receipt': 'test_order_001',
            'notes': {
                'test': 'true'
            }
        }
        
        order = razorpay_client.order.create(data=order_data)
        print(f"✅ Test order created successfully: {order['id']}")
        print(f"   Order ID: {order['id']}")
        print(f"   Amount: ₹{order['amount']/100}")
        print(f"   Currency: {order['currency']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Razorpay: {e}")
        return False

def test_payment_config():
    """Test payment configuration for frontend"""
    config = {
        'key': RAZORPAY_KEY_ID,
        'amount': 500,  # ₹5 in paise
        'currency': 'INR',
        'name': 'Lucky Draw Test',
        'description': 'Test Payment',
        'order_id': 'test_order_123',
        'prefill': {
            'name': 'Test User',
            'contact': '9876543210'
        },
        'theme': {
            'color': '#ffd700'
        }
    }
    
    print("✅ Payment configuration for frontend:")
    print(json.dumps(config, indent=2))
    return config

if __name__ == "__main__":
    print("🧪 Testing Razorpay Integration")
    print("=" * 40)
    
    # Test API connection
    if test_razorpay_connection():
        print("\n✅ Razorpay API is working correctly!")
        
        # Test payment config
        test_payment_config()
        
        print("\n🎯 Next Steps:")
        print("1. Visit http://localhost:5000")
        print("2. Fill in user details")
        print("3. Select tickets")
        print("4. Click 'Pay Now' button")
        print("5. Razorpay payment window should open")
        
    else:
        print("\n❌ Razorpay integration has issues!")
        print("Please check your API keys and internet connection.")

