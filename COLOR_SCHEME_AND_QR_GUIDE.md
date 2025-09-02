# 🎨 New Color Scheme & QR Code Guide

## ✅ **Color Scheme Updated!**

I've changed all pages from the old blue/purple theme to match your image's **red and golden theme**:

### 🎨 **New Color Palette:**

- **Primary Background**: Red (#DC2626) to Dark Red (#B91C1C) gradient
- **Accent Color**: Golden (#F59E0B)
- **Text**: White (#FFFFFF)
- **Form Backgrounds**: Semi-transparent white with red borders
- **Hover Effects**: Golden shadows and highlights

### 📱 **Pages Updated:**

1. ✅ **index.html** - Welcome page
2. ✅ **payment.html** - UPI payment page
3. ✅ **tickets.html** - Ticket selection page
4. ✅ **success.html** - Confirmation page

---

## 📱 **QR Code for Your Website**

I've created a **QR code generator** that creates a scannable code for your Lucky Draw website!

### 🚀 **How to Generate QR Code:**

#### **Option 1: Windows (Easiest)**

1. **Double-click** `setup_and_qr.bat`
2. **Wait** for packages to install
3. **QR code** will be generated automatically
4. **Website** will start automatically

#### **Option 2: Manual Commands**

```bash
# Install required packages
pip install -r requirements.txt

# Generate QR code
python generate_website_qr.py

# Start website
python app.py
```

### 📁 **QR Code Output:**

- **Styled QR Code**: `static/images/website_qr.png`
- **Simple QR Code**: `static/images/website_qr_simple.png`

### 🎯 **What the QR Code Does:**

- **When scanned** → Opens your Lucky Draw website
- **Works on any device** → Mobile, tablet, computer
- **No app needed** → Uses built-in camera QR scanner

---

## 🌐 **Website URLs:**

### **Local Development:**

- **Main Site**: `http://localhost:5000`
- **Admin Panel**: `http://localhost:5000/admin/pending_payments`
- **Payment Approval**: `http://localhost:5000/admin/payment_received/10`

### **When You Deploy Online:**

1. **Change URL** in `generate_website_qr.py`
2. **Replace** `http://localhost:5000` with your domain
3. **Regenerate** QR code for the new URL

---

## 🎨 **Color Scheme Details:**

### **Background Gradients:**

```css
/* Old (Blue) */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* New (Red) */
background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
```

### **Shadow Effects:**

```css
/* Old (Blue) */
box-shadow: 0 0 30px rgba(102, 126, 234, 0.3);

/* New (Red) */
box-shadow: 0 0 30px rgba(220, 38, 38, 0.3);
```

### **Hover Effects:**

```css
/* Old (Blue) */
box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);

/* New (Golden) */
box-shadow: 0 10px 25px rgba(245, 158, 11, 0.4);
```

---

## 📱 **QR Code Usage:**

### **For You (Admin):**

1. **Print the QR code** and display it prominently
2. **Share it digitally** on social media, WhatsApp, etc.
3. **Anyone can scan** to visit your Lucky Draw website

### **For Users:**

1. **Open camera app** on phone
2. **Point at QR code**
3. **Click notification** to open website
4. **Start booking tickets** immediately!

---

## 🚀 **Quick Start:**

### **Step 1: Generate QR Code**

```bash
# Windows
setup_and_qr.bat

# Linux/Mac
chmod +x setup_and_qr.sh
./setup_and_qr.sh
```

### **Step 2: Test QR Code**

1. **Save the generated QR code** (`website_qr.png`)
2. **Open camera app** on your phone
3. **Scan the QR code**
4. **Website should open** automatically!

### **Step 3: Share with Others**

- **Print and display** the QR code
- **Share digitally** via messaging apps
- **Add to business cards** or flyers

---

## 🎯 **Benefits:**

### ✅ **Professional Look:**

- **Consistent red theme** across all pages
- **Golden accents** for premium feel
- **Modern gradient** backgrounds

### ✅ **Easy Access:**

- **One scan** opens your website
- **No typing URLs** needed
- **Works on any device**

### ✅ **Marketing Tool:**

- **Physical display** at events
- **Digital sharing** on social media
- **Business promotion** material

---

## 🔧 **Customization:**

### **Change Colors:**

Edit the CSS in each template file:

```css
.gradient-bg {
  background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
}
```

### **Change Website URL:**

Edit `generate_website_qr.py`:

```python
website_url = "https://yourdomain.com"  # Change this
```

### **Regenerate QR Code:**

```bash
python generate_website_qr.py
```

---

## 🎉 **Summary:**

**✅ Color Scheme**: Updated to red/golden theme matching your image
**✅ QR Code**: Generated for easy website access
**✅ All Pages**: Consistent new design
**✅ Easy Setup**: One-click batch/shell scripts

**Your Lucky Draw website now has:**

- 🎨 **Professional red theme**
- 📱 **Scannable QR code**
- 🌐 **Easy mobile access**
- 🚀 **Modern design**

**Next step**: Run `setup_and_qr.bat` (Windows) or `./setup_and_qr.sh` (Linux/Mac) to generate your QR code! 🎯💰

