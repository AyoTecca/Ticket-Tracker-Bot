from flask import render_template
from app import app
from .utils import check_tickets, send_telegram_message

@app.route("/")
def home():
    return "Ticket Tracker Bot is running!"

@app.route("/check-tickets")
def trigger_check():
    check_tickets()
    return "Ticket check initiated!"

@app.route("/test-telegram")
def test_telegram():
    send_telegram_message("🚀 TEST: Bot is working!")
    return "Telegram test sent!"

@app.route("/config-check")
def config_check():
    from app.utils import get_telegram_config
    try:
        token, chat_id = get_telegram_config()
        return f"Config OK! Token: {token[:5]}...{token[-5:]}, Chat ID: {chat_id}"
    except Exception as e:
        return f"Config error: {str(e)}"