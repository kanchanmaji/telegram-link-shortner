"""
Admin Management
Handle admin operations and bot management
"""

import aiohttp
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

class AdminManager:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
        # List of authorized admin user IDs
        self.authorized_admins = [123456789]  # Add admin telegram IDs here

    def is_admin(self, telegram_id: int) -> bool:
        """Check if user is authorized admin"""
        return telegram_id in self.authorized_admins

    async def get_system_stats(self) -> Dict[str, Any]:
        """Get system-wide statistics"""
        # This would fetch from multiple endpoints
        return {
            "total_users": 150,
            "active_users": 120,
            "total_links": 500,
            "total_clicks": 2500,
            "pending_payments": 8,
            "total_revenue": 5000.0,
            "server_status": "online",
            "last_updated": datetime.utcnow().isoformat()
        }

    async def get_pending_payments(self) -> List[Dict[str, Any]]:
        """Get pending payment requests"""
        # This would fetch from payments API
        return [
            {
                "id": 1,
                "user_id": 123456789,
                "username": "john_doe",
                "amount": 100.0,
                "payment_proof": "/path/to/screenshot.jpg",
                "created_at": "2025-10-04 10:30:00",
                "status": "pending"
            }
        ]

    async def approve_payment(self, payment_id: int, admin_id: int) -> Dict[str, Any]:
        """Approve a payment request"""
        async with aiohttp.ClientSession() as session:
            try:
                payload = {
                    "payment_id": payment_id,
                    "action": "approve",
                    "admin_id": admin_id
                }

                async with session.put(
                    f"{self.api_base_url}/api/admin/payments/{payment_id}",
                    json=payload
                ) as response:
                    return await response.json()

            except Exception as e:
                return {"error": f"Failed to approve payment: {e}"}

    async def reject_payment(self, payment_id: int, admin_id: int, reason: str) -> Dict[str, Any]:
        """Reject a payment request"""
        async with aiohttp.ClientSession() as session:
            try:
                payload = {
                    "payment_id": payment_id,
                    "action": "reject",
                    "admin_id": admin_id,
                    "reason": reason
                }

                async with session.put(
                    f"{self.api_base_url}/api/admin/payments/{payment_id}",
                    json=payload
                ) as response:
                    return await response.json()

            except Exception as e:
                return {"error": f"Failed to reject payment: {e}"}

    async def broadcast_message(self, message: str, admin_id: int) -> Dict[str, Any]:
        """Send broadcast message to all users"""
        async with aiohttp.ClientSession() as session:
            try:
                payload = {
                    "message": message,
                    "admin_id": admin_id
                }

                async with session.post(
                    f"{self.api_base_url}/api/admin/broadcast",
                    json=payload
                ) as response:
                    return await response.json()

            except Exception as e:
                return {"error": f"Failed to send broadcast: {e}"}

    async def get_user_details(self, telegram_id: int) -> Dict[str, Any]:
        """Get detailed user information"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.api_base_url}/api/users/{telegram_id}") as response:
                    if response.status == 200:
                        return await response.json()
                    return {"error": "User not found"}

            except Exception as e:
                return {"error": f"Failed to fetch user details: {e}"}

    async def update_user_balance(self, telegram_id: int, amount: float, action: str) -> Dict[str, Any]:
        """Update user balance (add/deduct)"""
        async with aiohttp.ClientSession() as session:
            try:
                payload = {"amount": amount, "action": action}

                async with session.put(
                    f"{self.api_base_url}/api/users/{telegram_id}/balance",
                    json=payload
                ) as response:
                    return await response.json()

            except Exception as e:
                return {"error": f"Failed to update balance: {e}"}

    async def block_user(self, telegram_id: int, reason: str, admin_id: int) -> Dict[str, Any]:
        """Block a user"""
        # This would update user status in database
        return {
            "status": "success",
            "message": f"User {telegram_id} blocked successfully",
            "reason": reason,
            "blocked_by": admin_id,
            "blocked_at": datetime.utcnow().isoformat()
        }

    async def unblock_user(self, telegram_id: int, admin_id: int) -> Dict[str, Any]:
        """Unblock a user"""
        return {
            "status": "success",
            "message": f"User {telegram_id} unblocked successfully",
            "unblocked_by": admin_id,
            "unblocked_at": datetime.utcnow().isoformat()
        }

    async def delete_shortlink(self, short_code: str, admin_id: int) -> Dict[str, Any]:
        """Delete a shortlink (admin action)"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.delete(f"{self.api_base_url}/api/shortlinks/{short_code}") as response:
                    return await response.json()

            except Exception as e:
                return {"error": f"Failed to delete shortlink: {e}"}

    async def get_system_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent system logs"""
        # This would fetch from logging system
        return [
            {
                "timestamp": "2025-10-04 10:30:00",
                "level": "INFO",
                "message": "User 123456789 created shortlink",
                "module": "shortlink"
            },
            {
                "timestamp": "2025-10-04 10:25:00",
                "level": "WARN",
                "message": "High CPU usage detected",
                "module": "system"
            }
        ]

    async def cleanup_expired_links(self) -> Dict[str, Any]:
        """Clean up expired links"""
        # This would run cleanup job
        return {
            "status": "success",
            "deleted_links": 25,
            "freed_codes": 25,
            "cleanup_time": datetime.utcnow().isoformat()
        }

    async def generate_report(self, report_type: str, date_range: Dict[str, str]) -> Dict[str, Any]:
        """Generate various reports"""
        return {
            "report_type": report_type,
            "date_range": date_range,
            "data": {},
            "generated_at": datetime.utcnow().isoformat(),
            "generated_by": "admin"
        }

    def format_admin_message(self, title: str, data: Dict[str, Any]) -> str:
        """Format admin information message"""
        message = f"ðŸ”§ **{title}**\n\n"

        for key, value in data.items():
            if isinstance(value, (int, float)):
                message += f"â€¢ **{key.replace('_', ' ').title()}:** {value:,}\n"
            else:
                message += f"â€¢ **{key.replace('_', ' ').title()}:** {value}\n"

        return message

    async def send_admin_notification(self, admin_id: int, message: str):
        """Send notification to admin"""
        # This would send direct message to admin
        pass
