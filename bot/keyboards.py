"""
Telegram Bot Keyboards
All inline keyboard layouts for the bot
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_keyboard():
    """Main menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("ðŸ”— Make Shortlink", callback_data="make_shortlink"),
            InlineKeyboardButton("ðŸ“ Manage Links", callback_data="manage_links")
        ],
        [
            InlineKeyboardButton("ðŸ’° Wallet", callback_data="wallet"),
            InlineKeyboardButton("ðŸŽ§ Support", callback_data="support")
        ],
        [
            InlineKeyboardButton("ðŸ“‹ Terms & Conditions", callback_data="terms"),
            InlineKeyboardButton("ðŸ“Š Statistics", callback_data="stats")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_terms_keyboard():
    """Terms and conditions keyboard"""
    keyboard = [
        [InlineKeyboardButton("âœ… Accept Terms", callback_data="accept_terms")],
        [InlineKeyboardButton("ðŸ“‹ Read Full Terms", callback_data="full_terms")],
        [InlineKeyboardButton("ðŸ”™ Back to Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_wallet_keyboard():
    """Wallet management keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("âž• Add Balance", callback_data="add_balance"),
            InlineKeyboardButton("ðŸ“Š Transaction History", callback_data="transaction_history")
        ],
        [
            InlineKeyboardButton("ðŸ”„ Refresh Balance", callback_data="refresh_balance"),
            InlineKeyboardButton("ðŸ’³ Payment Methods", callback_data="payment_methods")
        ],
        [InlineKeyboardButton("ðŸ  Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_payment_methods_keyboard():
    """Payment methods selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("ðŸ“± UPI Payment", callback_data="payment_upi"),
            InlineKeyboardButton("ðŸ’³ Razorpay", callback_data="payment_razorpay")
        ],
        [
            InlineKeyboardButton("ðŸ§ Bank Transfer", callback_data="payment_bank"),
            InlineKeyboardButton("ðŸ“± Paytm", callback_data="payment_paytm")
        ],
        [InlineKeyboardButton("ðŸ”™ Back to Wallet", callback_data="wallet")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_link_management_keyboard():
    """Link management keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("ðŸ“Š View All Links", callback_data="view_all_links"),
            InlineKeyboardButton("ðŸ”— Create New Link", callback_data="create_new_link")
        ],
        [
            InlineKeyboardButton("ðŸ“ˆ Top Performing", callback_data="top_links"),
            InlineKeyboardButton("â° Expiring Soon", callback_data="expiring_links")
        ],
        [
            InlineKeyboardButton("ðŸ—‘ï¸ Delete Links", callback_data="delete_links"),
            InlineKeyboardButton("ðŸ“‹ Export Data", callback_data="export_data")
        ],
        [InlineKeyboardButton("ðŸ  Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_expiry_keyboard(url: str):
    """Expiry selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("No Expiry", callback_data=f"shorten_no_expiry_{url}"),
            InlineKeyboardButton("1 Day", callback_data=f"shorten_1_{url}")
        ],
        [
            InlineKeyboardButton("7 Days", callback_data=f"shorten_7_{url}"),
            InlineKeyboardButton("30 Days", callback_data=f"shorten_30_{url}")
        ],
        [
            InlineKeyboardButton("90 Days", callback_data=f"shorten_90_{url}"),
            InlineKeyboardButton("1 Year", callback_data=f"shorten_365_{url}")
        ],
        [InlineKeyboardButton("âŒ Cancel", callback_data="cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard():
    """Admin panel keyboard (for authorized users)"""
    keyboard = [
        [
            InlineKeyboardButton("ðŸ‘¥ Manage Users", callback_data="admin_users"),
            InlineKeyboardButton("ðŸ”— Manage Links", callback_data="admin_links")
        ],
        [
            InlineKeyboardButton("ðŸ’° Payments", callback_data="admin_payments"),
            InlineKeyboardButton("ðŸ“Š Statistics", callback_data="admin_stats")
        ],
        [
            InlineKeyboardButton("ðŸ“¢ Broadcast", callback_data="admin_broadcast"),
            InlineKeyboardButton("âš™ï¸ Settings", callback_data="admin_settings")
        ],
        [InlineKeyboardButton("ðŸ”™ Back to Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirmation_keyboard(action: str, item_id: str):
    """Confirmation keyboard for destructive actions"""
    keyboard = [
        [
            InlineKeyboardButton("âœ… Confirm", callback_data=f"confirm_{action}_{item_id}"),
            InlineKeyboardButton("âŒ Cancel", callback_data="cancel")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_pagination_keyboard(current_page: int, total_pages: int, callback_prefix: str):
    """Pagination keyboard for lists"""
    keyboard = []

    nav_buttons = []
    if current_page > 1:
        nav_buttons.append(InlineKeyboardButton("â¬…ï¸ Previous", callback_data=f"{callback_prefix}_{current_page-1}"))

    nav_buttons.append(InlineKeyboardButton(f"ðŸ“„ {current_page}/{total_pages}", callback_data="page_info"))

    if current_page < total_pages:
        nav_buttons.append(InlineKeyboardButton("Next âž¡ï¸", callback_data=f"{callback_prefix}_{current_page+1}"))

    keyboard.append(nav_buttons)
    keyboard.append([InlineKeyboardButton("ðŸ”™ Back", callback_data="main_menu")])

    return InlineKeyboardMarkup(keyboard)

def get_link_actions_keyboard(link_id: str):
    """Individual link actions keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("ðŸ“Š View Stats", callback_data=f"link_stats_{link_id}"),
            InlineKeyboardButton("âœï¸ Edit", callback_data=f"edit_link_{link_id}")
        ],
        [
            InlineKeyboardButton("ðŸ“‹ Copy Link", callback_data=f"copy_link_{link_id}"),
            InlineKeyboardButton("ðŸ”— QR Code", callback_data=f"qr_link_{link_id}")
        ],
        [
            InlineKeyboardButton("ðŸ—‘ï¸ Delete", callback_data=f"delete_link_{link_id}"),
            InlineKeyboardButton("ðŸ”™ Back", callback_data="manage_links")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_payment_amounts_keyboard():
    """Predefined payment amounts keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("â‚¹50", callback_data="amount_50"),
            InlineKeyboardButton("â‚¹100", callback_data="amount_100")
        ],
        [
            InlineKeyboardButton("â‚¹250", callback_data="amount_250"),
            InlineKeyboardButton("â‚¹500", callback_data="amount_500")
        ],
        [
            InlineKeyboardButton("â‚¹1000", callback_data="amount_1000"),
            InlineKeyboardButton("ðŸ’° Custom Amount", callback_data="amount_custom")
        ],
        [InlineKeyboardButton("ðŸ”™ Back", callback_data="wallet")]
    ]
    return InlineKeyboardMarkup(keyboard)
