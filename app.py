import os
from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8602077726:AAGfuGftcPUSGamtbqsz3YgZSjsilmPjGBs"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

@app.route('/', methods=['GET'])
def home():
    return "M.K POST GENERATION Bot is live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if "message" in data:
        message = data["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()
        
        if text.startswith("/start"):
            welcome_msg = (
                "👋 **Welcome to 𝐌.𝐊 𝐏𝐎𝐒𝐓 𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐈𝐎𝐍 Bot!**\n\n"
                "Channel ke liye ready-made post generate karne ke liye ye command use karein:\n"
                "`/post <wins> <losses>`\n\n"
                "💡 **Example:**\n`/post 3 0`"
            )
            send_message(chat_id, welcome_msg)
            
        elif text.startswith("/post"):
            try:
                parts = text.split()
                if len(parts) < 3:
                    send_message(chat_id, "⚠️ Sahi format use karein bhai!\nExample: `/post 3 0`")
                    return "OK", 200
                
                wins = int(parts[1])
                losses = int(parts[2])
                total_trades = wins + losses

                # Format numbers with leading zeros (jaise 03, 00)
                f_total = f"{total_trades:02d}"
                f_wins = f"{wins:02d}"
                f_losses = f"{losses:02d}"

                # Generate professional channel post text
                post_text = (
                    "👑⚡️ 𝐆𝐔𝐘𝐒 𝐓𝐎𝐃𝐀𝐘’𝐒 𝟏𝐒𝐓 𝐏𝐔𝐁𝐋𝐈𝐂 𝐒𝐄𝐒𝐒𝐈𝐎𝐍 𝐂𝐎𝐌𝐏𝐋𝐄𝐓𝐄𝐃 𝐒𝐔𝐂𝐂𝐄𝐒𝐒𝐅𝐔𝐋𝐋𝐘 🔥\n\n"
                    "𝐀𝐋𝐇𝐀𝐌𝐃𝐔𝐋𝐈𝐋𝐋𝐀𝐇 𝐆𝐑𝐄𝐀𝐓 𝐑𝐄𝐒𝐔𝐋𝐓𝐒 📈💞💞\n\n"
                    f"✉️ 𝐓𝐎𝐓𝐀𝐋 𝐓𝐑𝐀𝐃𝐄𝐒 : w{f_total}✅\n"
                    f"✉️ 𝐖𝐈𝐍 𝐓𝐑𝐀𝐃𝐄𝐒     : w{f_wins} ✅\n"
                    f"✉️ 𝐋𝐎𝐒𝐒 𝐓𝐑𝐀𝐃𝐄𝐒    : 𝟺{f_losses} ❌\n\n"
                    "🚀 Today session was 100% profitable — clean and perfect entries 🔥\n\n"
                    "👑 𝐍𝐞𝐱𝐭 𝐩𝐨𝐰𝐞𝐫𝐟𝐮𝐥 𝐬𝐞𝐬𝐬𝐢𝐨𝐧 𝐰𝐢𝐥𝐥 𝐛𝐞 𝐢𝐧 𝐕𝐈𝐏 𝐎𝐍𝐋𝐘 👑\n\n"
                    "💎 𝐖𝐚𝐧𝐭 𝐭𝐨 𝐣𝐨𝐢𝐧 𝐕𝐈𝐏? 𝐅𝐨𝐥𝐥𝐨𝐰 𝐭𝐡𝐞𝐬𝐞 𝐬𝐢𝐦𝐩𝐥𝐞 𝐬𝐭𝐞𝐩𝐬:💅💅💅\n\n"
                    "𝟏𝐒𝐓 𝐂𝐫𝐞𝐚𝐭𝐞 𝐚 𝐧𝐞𝐰 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐮𝐬𝐢𝐧𝐠 𝐨𝐮𝐫 𝐨𝐟𝐟𝐢𝐜𝐢𝐚𝐥 𝐐𝐮𝐨𝐭𝐞𝐱 𝐥𝐢𝐧𝐤 👇\n"
                    "https://broker-qx.pro/?lid=1614510\n"
                    "🔗🔗🔗🔗🔗🔗🔗🔗\n\n"
                    "𝟐𝐍𝐃 𝐃𝐞𝐩𝐨𝐬𝐢𝐭 𝐦𝐢𝐧𝐢𝐦𝐮𝐦 $𝟓𝟎 𝐚𝐧𝐝 𝐬𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 𝐓𝐫𝐚𝐝𝐞𝐫 𝐈𝐃 ✍️\n"
                    "💬 @MK_TRADER586✅\n\n"
                    "𝟑𝐑𝐃 𝐀𝐟𝐭𝐞𝐫 𝐯𝐞𝐫𝐢𝐟𝐢𝐜𝐚𝐭𝐢𝐨𝐧, 𝐲𝐨𝐮’𝐥𝐥 𝐛𝐞 𝐚𝐝𝐝𝐞𝐝 𝐭𝐨 𝐨𝐮𝐫 𝐕𝐈𝐏 𝐠𝐫𝐨𝐮𝐩 🙂👑🙂\n\n"
                    "🔮⚡️ 𝐃𝐨𝐧’𝐭 𝐦𝐢𝐬𝐬 𝐭𝐡𝐞 𝐧𝐞𝐱𝐭 𝐛𝐢𝐠 𝐨𝐩𝐩𝐨𝐫𝐭𝐮𝐧𝐢𝐭𝐲 — 𝐣𝐨𝐢𝐧 𝐧𝐨𝐰 ⚡️🔮"
                )
                
                send_message(chat_id, post_text)

            except Exception as e:
                send_message(chat_id, f"❌ Error: {str(e)}")

    return "OK", 200

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)
