# Foxcode Shorter - AI Link Shortener SaaS Telegram Bot

ðŸ”— **A complete SaaS solution for URL shortening with Telegram bot integration**

Created by: [codewithkanchan.com](https://codewithkanchan.com)

## ðŸŒŸ Features

### ðŸ¤– Telegram Bot
- **Interactive Menu System** - Button-based navigation
- **URL Shortening** - Convert long URLs to short branded links  
- **Wallet System** - User balance management
- **Payment Integration** - Manual payments with screenshot verification
- **Link Management** - View, track, and manage shortened links
- **Expiry Dates** - Set custom expiry for links
- **Click Analytics** - Track link performance
- **Terms & Conditions** - User agreement system

### ðŸš€ FastAPI Backend
- **RESTful API** - Complete API for all operations
- **SQLite Database** - Lightweight and fast
- **JWT Authentication** - Secure API access
- **Custom Domain** - Your own branded short URLs
- **Click Tracking** - Detailed analytics
- **Auto Cleanup** - Expired links management

### ðŸŽ›ï¸ Admin Panel (PHP)
- **Dark Mode UI** - Modern Bootstrap 5 interface
- **Dashboard** - Real-time statistics and overview
- **User Management** - Manage users, balances, status
- **Link Management** - View, edit, delete shortened links
- **Payment Processing** - Approve/reject payment requests
- **Broadcast System** - Send messages to all users
- **Domain Management** - Update custom domain settings

## ðŸ—ï¸ Project Structure

```
linkshortener-bot/
â”œâ”€â”€ backend/                 # FastAPI Backend
â”‚   â”œâ”€â”€ main.py             # Main FastAPI application
â”‚   â”œâ”€â”€ models.py           # SQLAlchemy models
â”‚   â”œâ”€â”€ database.py         # Database connection
â”‚   â”œâ”€â”€ utils.py            # Utility functions
â”‚   â””â”€â”€ config.json         # Configuration
â”œâ”€â”€ bot/                    # Telegram Bot
â”‚   â”œâ”€â”€ bot.py              # Main bot application
â”‚   â”œâ”€â”€ handlers.py         # Message handlers
â”‚   â”œâ”€â”€ keyboards.py        # Inline keyboards
â”‚   â”œâ”€â”€ wallet.py           # Wallet management
â”‚   â””â”€â”€ admin.py            # Admin functionality
â”œâ”€â”€ admin_panel/            # PHP Admin Panel
â”‚   â”œâ”€â”€ dashboard.php       # Main dashboard
â”‚   â”œâ”€â”€ login.php           # Admin login
â”‚   â”œâ”€â”€ users.php           # User management
â”‚   â”œâ”€â”€ shortlinks.php      # Link management
â”‚   â”œâ”€â”€ payments.php        # Payment processing
â”‚   â”œâ”€â”€ broadcast.php       # Message broadcasting
â”‚   â””â”€â”€ config.php          # PHP configuration
â”œâ”€â”€ database.sql            # Database schema
â”œâ”€â”€ requirements.txt        # Python dependencies
â”œâ”€â”€ .env.example           # Environment variables template
â””â”€â”€ README.md              # This file
```

## âš™ï¸ Installation & Setup

### 1. Prerequisites
- Python 3.8+
- PHP 8.0+
- SQLite 3
- Web server (Apache/Nginx) for admin panel
- Telegram Bot Token (from @BotFather)

### 2. Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/foxcode-shorter.git
cd foxcode-shorter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize database
python backend/database.py

# Run FastAPI server
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Telegram Bot Setup

```bash
# Create bot with @BotFather
# 1. Start chat with @BotFather
# 2. Send /newbot
# 3. Choose bot name and username
# 4. Copy the bot token

# Update bot token in .env file
BOT_TOKEN=your_bot_token_here

# Run the bot
cd bot
python bot.py
```

### 4. Admin Panel Setup

```bash
# Set up web server (example for Apache)
# Copy admin_panel/ to your web directory
cp -r admin_panel/ /var/www/html/foxcode-admin/

# Update database credentials in admin_panel/config.php
# Set up proper permissions
chmod 755 /var/www/html/foxcode-admin/
chmod 644 /var/www/html/foxcode-admin/*.php

# Access admin panel
# http://your-domain.com/foxcode-admin/
# Default login: admin / foxcode123
```

### 5. Custom Domain Setup

```bash
# 1. Point your domain to your server
# 2. Update CUSTOM_DOMAIN in .env
# 3. Set up SSL certificate
# 4. Configure web server to redirect to FastAPI
```

## ðŸ”§ Configuration

### Environment Variables (.env)
```env
# Bot Configuration
BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://your-domain.com/webhook

# Database
DATABASE_URL=sqlite:///./foxcode_shorter.db

# API Configuration  
API_BASE_URL=http://localhost:8000
CUSTOM_DOMAIN=https://foxcode.tk

# Payment Configuration
UPI_ID=your_upi_id@paytm
```

### Admin Panel Configuration
- Update `admin_panel/config.php` with your settings
- Change default admin credentials
- Set up database connection
- Configure payment methods

## ðŸ’³ Payment Integration

### Manual Payments (Default)
- Users send payment via UPI/Bank transfer
- Upload payment screenshot
- Admin approves/rejects manually

### Razorpay Integration (Optional)
```php
// Add Razorpay keys in config.php
define('RAZORPAY_KEY_ID', 'rzp_live_xxxxx');
define('RAZORPAY_KEY_SECRET', 'xxxxx');
```

### Cashfree Integration (Optional)
```php
// Add Cashfree keys in config.php  
define('CASHFREE_CLIENT_ID', 'xxxxx');
define('CASHFREE_CLIENT_SECRET', 'xxxxx');
```

## ðŸ“Š API Documentation

### Authentication
Most endpoints require authentication. Include bot token or JWT token in headers.

### Key Endpoints
- `POST /api/users` - Create user
- `GET /api/users/{telegram_id}` - Get user info
- `POST /api/shortlinks` - Create shortlink  
- `GET /{short_code}` - Redirect to original URL
- `GET /api/shortlinks/{telegram_id}` - Get user's links
- `POST /api/payments` - Create payment request

### Example API Call
```python
import requests

# Create shortlink
response = requests.post('http://localhost:8000/api/shortlinks', json={
    'telegram_id': 123456789,
    'original_url': 'https://example.com',
    'expiry_days': 30
})
```

## ðŸŽ¨ Customization

### Bot Messages
Edit messages in `bot/handlers.py`:
```python
welcome_text = f"""
ðŸŽ‰ Welcome to **Your Brand** - AI Link Shortener!
...
"""
```

### Admin Panel Theme  
Modify CSS in `admin_panel/assets/css/style.css` or update Bootstrap theme.

### Custom Domain
1. Update `CUSTOM_DOMAIN` in `.env`
2. Point domain A record to your server
3. Set up SSL certificate
4. Configure reverse proxy

## ðŸ”’ Security

### Best Practices
- Change default admin credentials
- Use strong passwords
- Enable HTTPS
- Regular database backups
- Keep dependencies updated
- Validate all user inputs
- Use CSRF tokens

### Database Security
```sql
-- Regular backups
sqlite3 foxcode_shorter.db ".backup backup_$(date +%Y%m%d).db"

-- Monitor logs
tail -f logs/app.log
```

## ðŸš€ Deployment

### VPS Deployment
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip nginx sqlite3 php8.0-fpm

# Set up systemd service for FastAPI
sudo nano /etc/systemd/system/foxcode-api.service

# Set up systemd service for bot
sudo nano /etc/systemd/system/foxcode-bot.service

# Configure Nginx
sudo nano /etc/nginx/sites-available/foxcode

# Enable and start services
sudo systemctl enable foxcode-api foxcode-bot nginx
sudo systemctl start foxcode-api foxcode-bot nginx
```

### Docker Deployment (Optional)
```dockerfile
# Dockerfile for FastAPI
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## ðŸ“ˆ Monitoring

### Health Checks
```bash
# API health
curl http://localhost:8000/

# Database status  
sqlite3 foxcode_shorter.db "SELECT COUNT(*) FROM users;"

# Bot status
ps aux | grep bot.py
```

### Logs
```bash
# FastAPI logs
tail -f logs/api.log

# Bot logs  
tail -f logs/bot.log

# Admin panel logs
tail -f /var/log/nginx/access.log
```

## ðŸ¤ Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ðŸ“ž Support

- **Email**: support@codewithkanchan.com
- **Telegram**: @codewithkanchan
- **Website**: [codewithkanchan.com](https://codewithkanchan.com)
- **Documentation**: [docs.codewithkanchan.com](https://docs.codewithkanchan.com)

## ðŸ“ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ðŸ™ Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [python-telegram-bot](https://python-telegram-bot.org/) - Telegram bot library
- [Bootstrap](https://getbootstrap.com/) - Frontend framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM

## ðŸŽ¯ Roadmap

- [ ] Mobile app for link management
- [ ] Advanced analytics dashboard  
- [ ] QR code generation
- [ ] Bulk link shortening
- [ ] API rate limiting
- [ ] Multi-language support
- [ ] Link categorization
- [ ] Custom aliases
- [ ] Link password protection
- [ ] Webhook notifications

---

**Made with â¤ï¸ by [codewithkanchan.com](https://codewithkanchan.com)**

> "Simplifying URL management, one short link at a time!"
