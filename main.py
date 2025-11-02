from flask import Flask, request
import csv
from datetime import datetime
import os

app = Flask(__name__)

VERIFY_TOKEN = "my_voice_is_my_password_verify_me"
CSV_FILE = "conversations.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w") as f:
        f.write("timestamp,facebook_user_id,message\n")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Invalid", 403
    
    if request.method == "POST":
        data = request.json
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                if "message" in event:
                    user_id = event["sender"]["id"]
                    msg = event["message"].get("text", "")
                    with open(CSV_FILE, "a") as f:
                        f.write(f'{datetime.now().isoformat()},{user_id},"{msg}"\n')
        return {"ok": True}, 200

if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 5000)))
