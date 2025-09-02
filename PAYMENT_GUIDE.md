# 💳 Real UPI Payment System Guide

## 🎯 Overview

Your Lucky Draw application now implements **real UPI payment verification**! Users must provide actual 12-digit transaction IDs from real payments to your UPI account `9353539771@pthdfc`.

## 📋 How It Works

### 1. **Setup Your QR Code**

- Save your actual UPI QR code image as `static/images/actual_upi_qr.png`
- The system will display this QR code on the payment page
- If the image is not found, it shows a fallback placeholder

### 2. **Payment Flow**

1. User selects tickets → calculates total (₹5 per ticket)
2. User scans your QR code with any UPI app
3. User pays the exact amount to `9353539771@pthdfc`
4. User gets a 12-digit transaction reference from their UPI app
5. User enters the transaction ID in the verification form
6. System validates the transaction ID format (exactly 12 digits)
7. System checks if the transaction ID exists in verified payments
8. If valid → booking confirmed, if invalid → payment failed

### 3. **Transaction Verification**

```python
# Valid transactions are stored in VALID_TRANSACTIONS dictionary
VALID_TRANSACTIONS = {
    "123456789012": {"amount": 15, "verified": True, "timestamp": "..."}
}
```

## 🔧 Admin Functions

### Adding Valid Transactions

After receiving a real payment, add the transaction ID to your system:

```
http://localhost:5000/add_transaction/123456789012/15
```

- `123456789012` = 12-digit transaction ID
- `15` = amount in rupees

### Example Usage

1. User pays ₹15 for 3 tickets
2. You receive payment with transaction ID `987654321098`
3. Add to system: `http://localhost:5000/add_transaction/987654321098/15`
4. User can now verify payment with ID `987654321098`

## ⚡ Key Features

### ✅ **Validation**

- Transaction ID must be exactly 12 digits
- Amount must match the ticket total
- Transaction must exist in your verified list

### ❌ **Error Handling**

- Invalid format: "Transaction ID must be exactly 12 digits"
- Not found: "Transaction ID not found in our system"
- Wrong amount: "Amount mismatch. Expected: ₹15, Found: ₹10"

### 🛡️ **Security**

- Prevents random/fake transaction IDs
- Only allows verified payments
- Matches exact amounts

## 🚀 Testing

### Test Scenario 1: Valid Payment

1. Add test transaction: `http://localhost:5000/add_transaction/111122223333/25`
2. User selects 5 tickets (₹25 total)
3. User enters transaction ID: `111122223333`
4. Result: ✅ Payment verified → booking confirmed

### Test Scenario 2: Invalid Payment

1. User selects 2 tickets (₹10 total)
2. User enters random ID: `999988887777`
3. Result: ❌ Payment failed → "Transaction ID not found"

### Test Scenario 3: Wrong Amount

1. Add transaction for ₹5: `http://localhost:5000/add_transaction/444455556666/5`
2. User selects 3 tickets (₹15 total)
3. User enters ID: `444455556666`
4. Result: ❌ Payment failed → "Amount mismatch"

## 📱 User Experience

### Payment Page Shows:

- Selected tickets display
- Total amount calculation
- Your actual UPI QR code
- Step-by-step payment instructions
- 12-digit transaction ID input with validation
- Real-time error messages

### Success Page Shows:

- Booking confirmation
- Selected ticket numbers
- Transaction reference
- Total amount paid

## 🎯 Next Steps

1. **Replace QR Code**: Save your actual QR code as `actual_upi_qr.png`
2. **Start Application**: Run `python app.py`
3. **Test Payment**: Use the add_transaction URL to add valid transactions
4. **Go Live**: Users can now make real payments to your UPI account!

---

**💡 Pro Tip**: After each real payment you receive, immediately add the transaction ID to your system using the `/add_transaction` URL so users can verify their payments instantly!
