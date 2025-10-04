"""
Wallet Management
Handle wallet operations, payments, and balance management
"""

import aiohttp
import json
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any

class WalletManager:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url

    async def get_user_balance(self, telegram_id: int) -> float:
        """Get user's current balance"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.api_base_url}/api/users/{telegram_id}") as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('balance', 0.0)
                    return 0.0
            except Exception as e:
                print(f"Error fetching balance: {e}")
                return 0.0

    async def create_payment_request(self, telegram_id: int, amount: float, 
                                   payment_proof: str) -> Dict[str, Any]:
        """Create a new payment request"""
        async with aiohttp.ClientSession() as session:
            try:
                payload = {
                    "telegram_id": telegram_id,
                    "amount": amount,
                    "payment_proof": payment_proof
                }

                async with session.post(
                    f"{self.api_base_url}/api/payments",
                    json=payload
                ) as response:
                    return await response.json()

            except Exception as e:
                return {"error": f"Failed to create payment request: {e}"}

    async def get_transaction_history(self, telegram_id: int) -> list:
        """Get user's transaction history"""
        # This would be implemented with a proper endpoint
        # For now, return mock data
        return [
            {
                "id": 1,
                "type": "credit",
                "amount": 100.0,
                "description": "Balance added via UPI",
                "date": "2025-10-01",
                "status": "completed"
            },
            {
                "id": 2,
                "type": "debit",
                "amount": 10.0,
                "description": "Link shortening",
                "date": "2025-10-02",
                "status": "completed"
            }
        ]

    def validate_amount(self, amount: float) -> tuple[bool, str]:
        """Validate payment amount"""
        if amount < 50:
            return False, "Minimum amount is â‚¹50"
        if amount > 10000:
            return False, "Maximum amount is â‚¹10,000"
        return True, "Valid amount"

    def format_currency(self, amount: float) -> str:
        """Format currency display"""
        return f"â‚¹{amount:.2f}"

    async def generate_upi_payment_link(self, amount: float, reference: str) -> str:
        """Generate UPI payment link"""
        upi_id = "foxcode@paytm"
        name = "Foxcode Shorter"
        return f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn=Payment for {reference}"

    async def process_razorpay_payment(self, telegram_id: int, amount: float) -> Dict[str, Any]:
        """Process Razorpay payment (placeholder)"""
        # This would integrate with Razorpay API
        return {
            "status": "pending",
            "payment_url": "https://razorpay.com/payment/...",
            "order_id": f"order_{telegram_id}_{int(datetime.now().timestamp())}"
        }

    async def verify_payment_screenshot(self, file_path: str) -> Dict[str, Any]:
        """Verify payment screenshot (placeholder for ML/AI verification)"""
        # This could use OCR or AI to verify payment screenshots
        # For now, return manual verification required
        return {
            "auto_verified": False,
            "confidence": 0.0,
            "extracted_amount": None,
            "extracted_upi_id": None,
            "requires_manual_review": True
        }

    def calculate_links_from_balance(self, balance: float, link_cost: float = 10.0) -> int:
        """Calculate how many links can be created with current balance"""
        return int(balance // link_cost)

    def format_transaction_message(self, transaction: Dict[str, Any]) -> str:
        """Format transaction for display"""
        emoji = "ðŸ’š" if transaction['type'] == 'credit' else "ðŸ’¸"
        amount_text = f"+{transaction['amount']}" if transaction['type'] == 'credit' else f"-{transaction['amount']}"

        return f"{emoji} **{amount_text}** - {transaction['description']}\nðŸ“… {transaction['date']}"

    async def get_payment_methods(self) -> list:
        """Get available payment methods"""
        return [
            {
                "id": "upi",
                "name": "UPI Payment",
                "icon": "ðŸ“±",
                "enabled": True,
                "min_amount": 50,
                "max_amount": 10000,
                "processing_time": "Instant (after verification)"
            },
            {
                "id": "razorpay",
                "name": "Card/Net Banking",
                "icon": "ðŸ’³",
                "enabled": False,  # Coming soon
                "min_amount": 50,
                "max_amount": 50000,
                "processing_time": "Instant"
            },
            {
                "id": "bank_transfer",
                "name": "Bank Transfer",
                "icon": "ðŸ§",
                "enabled": True,
                "min_amount": 100,
                "max_amount": 100000,
                "processing_time": "1-2 business days"
            }
        ]

    async def send_payment_reminder(self, telegram_id: int, payment_id: int):
        """Send payment reminder to user"""
        # This would be implemented with the bot instance
        pass

    async def process_refund(self, payment_id: int, reason: str) -> Dict[str, Any]:
        """Process payment refund"""
        # This would implement refund logic
        return {
            "status": "success",
            "refund_id": f"refund_{payment_id}_{int(datetime.now().timestamp())}",
            "amount_refunded": 0.0,
            "processing_time": "3-5 business days"
        }
