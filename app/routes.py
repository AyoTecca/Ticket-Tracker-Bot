from flask import render_template
from app import app
from .utils import check_tickets  # Add this import

@app.route("/")
def home():
    return "Ticket Tracker Bot is running!"

# Add new endpoint
@app.route("/check-tickets")
def trigger_check():
    check_tickets()
    return "Ticket check initiated!"