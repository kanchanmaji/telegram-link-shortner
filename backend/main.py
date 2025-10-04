"""
Foxcode Shorter - AI Link Shortener SaaS Backend
FastAPI + SQLite Backend API for Telegram Bot
Created by: codewithkanchan.com
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db
from models import User, Shortlink, Payment, Base
import utils
import json
import os
from datetime import datetime, timedelta
from typing import Optional

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

app = FastAPI(
    title="Foxcode Shorter API",
    description="AI Link Shortener SaaS Backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Foxcode Shorter API", "status": "running", "version": "1.0.0"}

@app.post("/api/users")
def create_user(telegram_id: int, username: str, db: Session = Depends(get_db)):
    """Create new user"""
    try:
        existing_user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if existing_user:
            return {"message": "User already exists", "user_id": existing_user.id}

        new_user = User(
            telegram_id=telegram_id,
            username=username,
            balance=0,
            status="active"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User created successfully", "user_id": new_user.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/users/{telegram_id}")
def get_user(telegram_id: int, db: Session = Depends(get_db)):
    """Get user information"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "balance": user.balance,
        "status": user.status,
        "created_at": user.created_at
    }

@app.post("/api/shortlinks")
def create_shortlink(telegram_id: int, original_url: str, 
                    expiry_days: Optional[int] = None, db: Session = Depends(get_db)):
    """Create new shortlink"""
    try:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.balance < config["shortlink_cost"]:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        # Generate unique short code
        short_code = utils.generate_short_code()
        while db.query(Shortlink).filter(Shortlink.short_code == short_code).first():
            short_code = utils.generate_short_code()

        # Calculate expiry date
        expiry_date = None
        if expiry_days:
            expiry_date = datetime.utcnow() + timedelta(days=expiry_days)

        # Create shortlink
        shortlink = Shortlink(
            user_id=user.id,
            original_url=original_url,
            short_code=short_code,
            expiry_date=expiry_date,
            clicks=0,
            status="active"
        )
        db.add(shortlink)

        # Deduct balance
        user.balance -= config["shortlink_cost"]
        db.commit()
        db.refresh(shortlink)

        short_url = f"{config['custom_domain']}/{short_code}"

        return {
            "message": "Shortlink created successfully",
            "short_url": short_url,
            "short_code": short_code,
            "expiry_date": expiry_date,
            "remaining_balance": user.balance
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{short_code}")
def redirect_shortlink(short_code: str, db: Session = Depends(get_db)):
    """Redirect to original URL"""
    try:
        shortlink = db.query(Shortlink).filter(
            Shortlink.short_code == short_code,
            Shortlink.status == "active"
        ).first()

        if not shortlink:
            raise HTTPException(status_code=404, detail="Short URL not found")

        # Check expiry
        if shortlink.expiry_date and datetime.utcnow() > shortlink.expiry_date:
            shortlink.status = "expired"
            db.commit()
            raise HTTPException(status_code=404, detail="Short URL has expired")

        # Increment click count
        shortlink.clicks += 1
        shortlink.last_clicked = datetime.utcnow()
        db.commit()

        return RedirectResponse(url=shortlink.original_url)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/shortlinks/{telegram_id}")
def get_user_shortlinks(telegram_id: int, db: Session = Depends(get_db)):
    """Get user's shortlinks"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    shortlinks = db.query(Shortlink).filter(Shortlink.user_id == user.id).all()

    result = []
    for link in shortlinks:
        result.append({
            "id": link.id,
            "original_url": link.original_url,
            "short_url": f"{config['custom_domain']}/{link.short_code}",
            "short_code": link.short_code,
            "clicks": link.clicks,
            "status": link.status,
            "created_at": link.created_at,
            "expiry_date": link.expiry_date,
            "last_clicked": link.last_clicked
        })

    return {"shortlinks": result}

@app.post("/api/payments")
def create_payment_request(telegram_id: int, amount: float, 
                          payment_proof: str, db: Session = Depends(get_db)):
    """Create payment request"""
    try:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        payment = Payment(
            user_id=user.id,
            amount=amount,
            payment_proof=payment_proof,
            status="pending"
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)

        return {
            "message": "Payment request submitted successfully",
            "payment_id": payment.id,
            "status": "pending"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/users/{telegram_id}/balance")
def update_user_balance(telegram_id: int, amount: float, 
                       action: str, db: Session = Depends(get_db)):
    """Update user balance (admin only)"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if action == "add":
        user.balance += amount
    elif action == "deduct":
        user.balance = max(0, user.balance - amount)
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    db.commit()

    return {
        "message": "Balance updated successfully",
        "new_balance": user.balance
    }

@app.delete("/api/shortlinks/{short_code}")
def delete_shortlink(short_code: str, db: Session = Depends(get_db)):
    """Delete shortlink (admin only)"""
    shortlink = db.query(Shortlink).filter(Shortlink.short_code == short_code).first()
    if not shortlink:
        raise HTTPException(status_code=404, detail="Shortlink not found")

    db.delete(shortlink)
    db.commit()

    return {"message": "Shortlink deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
