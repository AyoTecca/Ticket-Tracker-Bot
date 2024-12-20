from flask import render_template
from app import app

@app.route("/")
def home():
    return "Ticket Tracker Bot is running!"
