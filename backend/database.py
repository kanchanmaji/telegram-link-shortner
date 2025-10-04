"""
Database connection and session management
SQLAlchemy database setup for SQLite
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./foxcode_shorter.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """Initialize database with default settings"""
    create_tables()

    # Add default settings
    from models import Settings, Admin
    from utils import hash_password

    db = SessionLocal()
    try:
        # Default settings
        default_settings = [
            {"key": "shortlink_cost", "value": "10", "description": "Cost per shortlink in rupees"},
            {"key": "custom_domain", "value": "https://foxcode.tk", "description": "Custom domain for shortlinks"},
            {"key": "bot_token", "value": "YOUR_BOT_TOKEN", "description": "Telegram bot token"},
            {"key": "razorpay_key_id", "value": "rzp_test_xxxxx", "description": "Razorpay key ID"},
            {"key": "razorpay_key_secret", "value": "xxxxx", "description": "Razorpay key secret"},
            {"key": "qr_payment_upi", "value": "foxcode@paytm", "description": "UPI ID for QR payments"}
        ]

        for setting in default_settings:
            existing = db.query(Settings).filter(Settings.key == setting["key"]).first()
            if not existing:
                new_setting = Settings(**setting)
                db.add(new_setting)

        # Default admin
        existing_admin = db.query(Admin).filter(Admin.username == "admin").first()
        if not existing_admin:
            admin = Admin(
                username="admin",
                email="admin@foxcode.com",
                password_hash=hash_password("foxcode123"),
                role="super_admin"
            )
            db.add(admin)

        db.commit()
        print("âœ… Database initialized with default settings")

    except Exception as e:
        print(f"âŒ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
