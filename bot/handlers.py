"""
Telegram Bot Handlers
All command and message handlers for the bot
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from keyboards import *
from wallet import WalletManager
import re

# User state storage (in production, use Redis or database)
user_states = {}

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user

    # Register user in backend
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{context.bot_data.get('api_base_url', 'http://localhost:8000')}/api/users",
                json={"telegram_id": user.id, "username": user.username or str(user.id)}
            ) as response:
                data = await response.json()
        except Exception as e:
            print(f"Error registering user: {e}")

    welcome_text = f"""
ðŸŽ‰ Welcome to **Foxcode Shorter** - AI Link Shortener SaaS!

ðŸ‘‹ Hello {user.first_name}!

ðŸ”— **What we do:**
â€¢ Convert long URLs to short, branded links
â€¢ Track clicks and analytics
â€¢ Custom domain support
â€¢ Expiry date management

ðŸ’° **Cost:** â‚¹10 per short link

âš¡ **Quick Start:**
1. Accept our Terms & Conditions
2. Add balance to your wallet
3. Send any URL to shorten it

Choose an option below to get started:
    """

    keyboard = get_main_keyboard()

    await update.message.reply_text(
        welcome_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
ðŸ¤– **Foxcode Shorter Bot Help**

**Commands:**
â€¢ `/start` - Start the bot and see main menu
â€¢ `/help` - Show this help message
â€¢ `/shorten <url>` - Shorten a URL directly
â€¢ `/manage` - Manage your shortened links
â€¢ `/wallet` - Check wallet balance and add funds
â€¢ `/terms` - View Terms & Conditions
â€¢ `/stats` - View your statistics
â€¢ `/support` - Get support

**How to use:**
1. **Shorten URLs:** Just send any URL in chat
2. **Add Balance:** Use wallet menu to add funds
3. **Track Links:** View clicks and stats in manage section
4. **Set Expiry:** Choose expiry date for your links

**Pricing:**
â€¢ â‚¹10 per shortened link
â€¢ No subscription fees
â€¢ Pay as you use

**Support:**
Contact @codewithkanchan for help and support.

Made with â¤ï¸ by codewithkanchan.com
    """

    await update.message.reply_text(
        help_text,
        parse_mode=ParseMode.MARKDOWN
    )

async def shorten_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /shorten command with URL"""
    if not context.args:
        await update.message.reply_text(
            "âŒ Please provide a URL to shorten.\n\n**Usage:** `/shorten https://example.com`",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    url = context.args[0]
    user_id = update.effective_user.id

    # Validate URL
    if not is_valid_url(url):
        await update.message.reply_text("âŒ Please provide a valid URL starting with http:// or https://")
        return

    # Ask for expiry
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("No Expiry", callback_data=f"shorten_no_expiry_{url}"),
            InlineKeyboardButton("7 Days", callback_data=f"shorten_7_{url}")
        ],
        [
            InlineKeyboardButton("30 Days", callback_data=f"shorten_30_{url}"),
            InlineKeyboardButton("90 Days", callback_data=f"shorten_90_{url}")
        ],
        [InlineKeyboardButton("âŒ Cancel", callback_data="cancel")]
    ])

    await update.message.reply_text(
        f"ðŸ”— **URL to shorten:** `{url}`\n\nâ° Choose expiry period:",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def manage_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /manage command"""
    user_id = update.effective_user.id

    # Get user's shortlinks from backend
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{context.bot_data.get('api_base_url', 'http://localhost:8000')}/api/shortlinks/{user_id}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    shortlinks = data.get('shortlinks', [])
                else:
                    shortlinks = []
        except Exception as e:
            await update.message.reply_text("âŒ Error fetching your links. Please try again.")
            return

    if not shortlinks:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ðŸ”— Create First Link", callback_data="create_first_link")]
        ])

        await update.message.reply_text(
            "ðŸ“ **Your Shortened Links**\n\nâŒ No links found.\n\nCreate your first shortened link!",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Show links with pagination
    text = "ðŸ“ **Your Shortened Links:**\n\n"

    for i, link in enumerate(shortlinks[:5], 1):  # Show first 5
        status_emoji = "âœ…" if link['status'] == 'active' else "âŒ"
        text += f"{status_emoji} **Link {i}**\n"
        text += f"ðŸ”— `{link['short_url']}`\n"
        text += f"ðŸ“Š {link['clicks']} clicks\n"
        text += f"ðŸ“… Created: {link['created_at'][:10]}\n"
        if link['expiry_date']:
            text += f"â° Expires: {link['expiry_date'][:10]}\n"
        text += "\n"

    if len(shortlinks) > 5:
        text += f"... and {len(shortlinks) - 5} more links\n"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ðŸ“Š View All", callback_data="view_all_links"),
            InlineKeyboardButton("ðŸ”— New Link", callback_data="create_new_link")
        ],
        [InlineKeyboardButton("ðŸ  Main Menu", callback_data="main_menu")]
    ])

    await update.message.reply_text(
        text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def wallet_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /wallet command"""
    user_id = update.effective_user.id

    # Get user info from backend
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{context.bot_data.get('api_base_url', 'http://localhost:8000')}/api/users/{user_id}"
            ) as response:
                if response.status == 200:
                    user_data = await response.json()
                    balance = user_data.get('balance', 0)
                else:
                    balance = 0
        except Exception as e:
            await update.message.reply_text("âŒ Error fetching wallet info. Please try again.")
            return

    wallet_text = f"""
ðŸ’° **Your Wallet**

ðŸ’µ **Current Balance:** â‚¹{balance:.2f}
ðŸ”— **Links you can create:** {int(balance // 10)} links

ðŸ“Š **Pricing:**
â€¢ â‚¹10 per shortened link
â€¢ No hidden charges
â€¢ Instant processing

ðŸ’³ **Add Balance:**
Choose payment method below
    """

    keyboard = get_wallet_keyboard()

    await update.message.reply_text(
        wallet_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def support_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /support command"""
    support_text = """
ðŸŽ§ **Support & Help**

**Need help?** We're here for you!

ðŸ“ž **Contact Options:**
â€¢ Telegram: @codewithkanchan
â€¢ Email: support@codewithkanchan.com
â€¢ Website: codewithkanchan.com

â“ **Common Issues:**
â€¢ **Can't shorten URL?** Check if URL is valid and you have balance
â€¢ **Payment issues?** Contact support with payment screenshot
â€¢ **Link not working?** Check if link has expired

â° **Support Hours:**
Monday to Friday: 9 AM - 6 PM IST
Response time: Within 24 hours

ðŸ› **Report Bugs:**
Found a bug? Please report it to help us improve!

**Made with â¤ï¸ by codewithkanchan.com**
    """

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ðŸ“ž Contact Support", url="https://t.me/codewithkanchan")],
        [InlineKeyboardButton("ðŸŒ Visit Website", url="https://codewithkanchan.com")],
        [InlineKeyboardButton("ðŸ  Main Menu", callback_data="main_menu")]
    ])

    await update.message.reply_text(
        support_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def terms_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /terms command"""
    terms_text = """
ðŸ“‹ **Terms & Conditions**

**By using Foxcode Shorter, you agree to:**

ðŸš« **Prohibited Content:**
â€¢ No illegal or phishing links
â€¢ No adult, piracy, or spam content
â€¢ No malware or harmful websites
â€¢ No copyright infringing material

ðŸ’° **Pricing & Payments:**
â€¢ â‚¹10 per shortened link
â€¢ Balance deducted automatically
â€¢ No refunds for processed links
â€¢ Unused balance remains in wallet

â° **Link Management:**
â€¢ Expired links are auto-deleted
â€¢ No guarantee of permanent storage
â€¢ Users responsible for backup
â€¢ Custom expiry dates available

ðŸ”’ **Privacy & Data:**
â€¢ We collect minimal user data
â€¢ Click analytics are anonymous
â€¢ Data used only for service provision
â€¢ No data sold to third parties

âš–ï¸ **Service Terms:**
â€¢ Service provided "as is"
â€¢ We reserve right to suspend accounts
â€¢ Terms may be updated without notice
â€¢ Disputes resolved under Indian law

**Last updated:** October 2025
**Contact:** support@codewithkanchan.com
    """

    keyboard = get_terms_keyboard()

    await update.message.reply_text(
        terms_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    user_id = update.effective_user.id

    # Get user stats from backend
    async with aiohttp.ClientSession() as session:
        try:
            # Get user info
            async with session.get(
                f"{context.bot_data.get('api_base_url', 'http://localhost:8000')}/api/users/{user_id}"
            ) as response:
                user_data = await response.json() if response.status == 200 else {}

            # Get shortlinks
            async with session.get(
                f"{context.bot_data.get('api_base_url', 'http://localhost:8000')}/api/shortlinks/{user_id}"
            ) as response:
                links_data = await response.json() if response.status == 200 else {"shortlinks": []}

        except Exception as e:
            await update.message.reply_text("âŒ Error fetching statistics. Please try again.")
            return

    shortlinks = links_data.get('shortlinks', [])
    total_links = len(shortlinks)
    total_clicks = sum(link.get('clicks', 0) for link in shortlinks)
    active_links = len([link for link in shortlinks if link.get('status') == 'active'])
    expired_links = len([link for link in shortlinks if link.get('status') == 'expired'])

    stats_text = f"""
ðŸ“Š **Your Statistics**

ðŸ‘¤ **Account Info:**
â€¢ Member since: {user_data.get('created_at', 'N/A')[:10]}
â€¢ Current balance: â‚¹{user_data.get('balance', 0):.2f}
â€¢ Account status: {user_data.get('status', 'N/A').title()}

ðŸ”— **Link Statistics:**
â€¢ Total links created: {total_links}
â€¢ Active links: {active_links}
â€¢ Expired links: {expired_links}

ðŸ“ˆ **Performance:**
â€¢ Total clicks: {total_clicks:,}
â€¢ Average clicks per link: {total_clicks/max(total_links, 1):.1f}

ðŸ’° **Spending:**
â€¢ Amount spent: â‚¹{total_links * 10:.2f}
â€¢ Links available: {int(user_data.get('balance', 0) // 10)}
    """

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ðŸ“ Manage Links", callback_data="manage_links"),
            InlineKeyboardButton("ðŸ’° Add Balance", callback_data="add_balance")
        ],
        [InlineKeyboardButton("ðŸ  Main Menu", callback_data="main_menu")]
    ])

    await update.message.reply_text(
        stats_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def url_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle URL messages"""
    text = update.message.text.strip()

    # Check if it's a valid URL
    if not is_valid_url(text):
        # If not a URL, ignore or provide help
        return

    user_id = update.effective_user.id

    # Check if user accepted terms
    if not user_states.get(user_id, {}).get('terms_accepted'):
        keyboard = get_terms_keyboard()
        await update.message.reply_text(
            "âš ï¸ Please accept our Terms & Conditions first before using the service.",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )
        return

    # Ask for expiry period
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("No Expiry", callback_data=f"shorten_no_expiry_{text}"),
            InlineKeyboardButton("7 Days", callback_data=f"shorten_7_{text}")
        ],
        [
            InlineKeyboardButton("30 Days", callback_data=f"shorten_30_{text}"),
            InlineKeyboardButton("90 Days", callback_data=f"shorten_90_{text}")
        ],
        [InlineKeyboardButton("âŒ Cancel", callback_data="cancel")]
    ])

    await update.message.reply_text(
        f"ðŸ”— **URL detected:** `{text}`\n\nâ° Choose expiry period:\nðŸ’° Cost: â‚¹10",
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = query.from_user.id

    if data == "main_menu":
        keyboard = get_main_keyboard()
        await query.edit_message_text(
            "ðŸ  **Main Menu**\n\nChoose an option:",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )

    elif data == "accept_terms":
        user_states[user_id] = user_states.get(user_id, {})
        user_states[user_id]['terms_accepted'] = True

        await query.edit_message_text(
            "âœ… **Terms Accepted!**\n\nYou can now use all features of Foxcode Shorter.\n\nðŸ”— Send any URL to get started!",
            parse_mode=ParseMode.MARKDOWN
        )

    elif data.startswith("shorten_"):
        # Handle shortening with expiry
        parts = data.split("_", 2)
        expiry = parts[1]
        url = parts[2] if len(parts) > 2 else ""

        if expiry == "no":
            expiry_days = None
        else:
            expiry_days = int(expiry)

        await process_url_shortening(query, url, expiry_days, context)

    elif data == "add_balance":
        keyboard = get_payment_methods_keyboard()
        await query.edit_message_text(
            "ðŸ’³ **Add Balance**\n\nChoose payment method:",
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN
        )

    elif data.startswith("payment_"):
        payment_method = data.split("_")[1]
        await handle_payment_method(query, payment_method, context)

async def process_url_shortening(query, url: str, expiry_days: int, context):
    """Process URL shortening request"""
    user_id = query.from_user.id

    # Show processing message
    await query.edit_message_text("ðŸ”„ Processing your request...")

    # Make API request to backend
    async with aiohttp.ClientSession() as session:
        try:
            payload = {
                "telegram_id": user_id,
                "original_url": url,
                "expiry_days": expiry_days
            }

            async with session.post(
                f"{context.bot_data.get('api_base_url', 'http://localhost:8000')}/api/shortlinks",
                json=payload
            ) as response:
                result = await response.json()

                if response.status == 200:
                    short_url = result['short_url']
                    remaining_balance = result['remaining_balance']
                    expiry_text = f"â° Expires: {result['expiry_date'][:10]}" if result['expiry_date'] else "â™¾ï¸ No expiry"

                    success_text = f"""
âœ… **Link shortened successfully!**

ðŸ”— **Your short URL:** `{short_url}`
ðŸ“‹ **Original URL:** `{url}`
{expiry_text}
ðŸ’° **Remaining balance:** â‚¹{remaining_balance:.2f}

**Share your short link anywhere!**
                    """

                    keyboard = InlineKeyboardMarkup([
                        [InlineKeyboardButton("ðŸ“‹ Copy Link", url=short_url)],
                        [
                            InlineKeyboardButton("ðŸ“ Manage Links", callback_data="manage_links"),
                            InlineKeyboardButton("ðŸ”— Shorten Another", callback_data="shorten_another")
                        ],
                        [InlineKeyboardButton("ðŸ  Main Menu", callback_data="main_menu")]
                    ])

                    await query.edit_message_text(
                        success_text,
                        reply_markup=keyboard,
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    error_msg = result.get('detail', 'Unknown error occurred')
                    await query.edit_message_text(
                        f"âŒ **Error:** {error_msg}\n\nPlease try again or contact support.",
                        parse_mode=ParseMode.MARKDOWN
                    )

        except Exception as e:
            await query.edit_message_text(
                "âŒ **Network Error**\n\nPlease check your connection and try again.",
                parse_mode=ParseMode.MARKDOWN
            )

async def handle_payment_method(query, method: str, context):
    """Handle different payment methods"""
    if method == "upi":
        payment_text = """
ðŸ’³ **UPI Payment**

**Steps to add balance:**
1. Pay to UPI ID: `foxcode@paytm`
2. Take screenshot of payment
3. Send screenshot to bot
4. Wait for admin approval

**Note:** Minimum amount â‚¹50
        """

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ðŸ“¸ Send Screenshot", callback_data="send_screenshot")],
            [InlineKeyboardButton("ðŸ”™ Back", callback_data="add_balance")]
        ])

    elif method == "razorpay":
        payment_text = "ðŸ’³ **Razorpay Integration** (Coming Soon!)\n\nCurrently under development."
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ðŸ”™ Back", callback_data="add_balance")]
        ])

    else:
        payment_text = "âŒ Invalid payment method"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("ðŸ”™ Back", callback_data="add_balance")]
        ])

    await query.edit_message_text(
        payment_text,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )

def is_valid_url(url: str) -> bool:
    """Basic URL validation"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
        r'[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None
