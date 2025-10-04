"""
Utility functions for Foxcode Shorter
Helper functions for short code generation, password hashing, etc.
"""

import string
import random
import hashlib
import bcrypt
import re
from datetime import datetime, timedelta
import qrcode
import io
import base64
from urllib.parse import urlparse

def generate_short_code(length=8):
    """Generate random short code for URLs"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def is_valid_url(url: str) -> bool:
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def clean_url(url: str) -> str:
    """Clean and format URL"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def generate_qr_code(text: str) -> str:
    """Generate QR code and return base64 string"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return ""

def format_currency(amount: float) -> str:
    """Format currency in Indian Rupees"""
    return f"â‚¹{amount:.2f}"

def time_ago(dt: datetime) -> str:
    """Get human-readable time difference"""
    now = datetime.utcnow()
    diff = now - dt

    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hours ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minutes ago"
    else:
        return "Just now"

def validate_telegram_id(telegram_id: str) -> bool:
    """Validate Telegram ID format"""
    return telegram_id.isdigit() and len(telegram_id) >= 9

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

def generate_payment_reference() -> str:
    """Generate unique payment reference"""
    timestamp = str(int(datetime.utcnow().timestamp()))
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"FXC{timestamp}{random_part}"

def calculate_expiry_date(days: int) -> datetime:
    """Calculate expiry date from current date"""
    return datetime.utcnow() + timedelta(days=days)

def is_expired(expiry_date: datetime) -> bool:
    """Check if date has expired"""
    return datetime.utcnow() > expiry_date

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"

    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f}{size_names[i]}"

def create_payment_qr_data(upi_id: str, amount: float, name: str = "Foxcode Shorter") -> str:
    """Create UPI payment QR code data"""
    return f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn=Payment for Foxcode Shorter"

def log_activity(user_id: int, action: str, details: str = ""):
    """Log user activity (can be extended to database logging)"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] User {user_id}: {action} {details}")
