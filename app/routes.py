from flask import render_template
from app import app
from .utils import check_tickets  # Add this import
from .utils import send_telegram_message

@app.route("/")
def home():
    return "Ticket Tracker Bot is running!"

# Add new endpoint
@app.route("/check-tickets")
def trigger_check():
    check_tickets()
    return "Ticket check initiated!"

# Add this new test route
@app.route("/test-telegram")
def test_telegram():
    test_message = "🚀 Test message from Ticket Tracker Bot!"
    send_telegram_message(test_message)
    return "Test message sent to Telegram!"

@app.route("/debug")
def debug():
    import os
    debug_info = {
        "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN", "NOT SET"),
        "CHAT_ID": os.getenv("CHAT_ID", "NOT SET"),
        "bot_status": "✅ Environment variables loaded" if os.getenv("TELEGRAM_TOKEN") else "❌ Missing variables"
    }
    return debug_info