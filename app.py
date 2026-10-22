import os
from flask import Flask, request
import requests
from PIL import Image, ImageDraw, ImageFont

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
                "Trading P&L Card banane ke liye ye format use karein:\n"
                "`/pnl <wins> <losses> <profit>`\n\n"
                "💡 **Example:**\n`/pnl 8 2 450`"
            )
            send_message(chat_id, welcome_msg)
            
        elif text.startswith("/pnl"):
            try:
                parts = text.split()
                if len(parts) < 4:
                    send_message(chat_id, "⚠️ Sahi format use karein bhai!\nExample: `/pnl 8 2 450`")
                    return "OK", 200
                
                wins = int(parts[1])
                losses = int(parts[2])
                profit = parts[3]
                
                total_trades = wins + losses
                win_rate = round((wins / total_trades) * 100, 1) if total_trades > 0 else 0

                # Create P&L Image Canvas (Dark Professional Trading Theme)
                img_width, img_height = 800, 500
                background_color = (15, 23, 42)  # Dark Navy/Slate
                image = Image.new("RGB", (img_width, img_height), color=background_color)
                draw = ImageDraw.Draw(image)

                # Load Fonts (Using default fallback safely for serverless environment)
                try:
                    font_title = ImageFont.truetype("arial.ttf", 32)
                    font_body = ImageFont.truetype("arial.ttf", 24)
                except:
                    font_title = ImageFont.load_default()
                    font_body = ImageFont.load_default()

                # Draw Card Content
                draw.text((50, 40), "M.K TRADER — DAILY P&L REPORT", fill=(0, 255, 150), font=font_title)
                draw.line([(50, 90), (750, 90)], fill=(51, 65, 85), width=2)

                draw.text((50, 130), f"📊 Total Trades: {total_trades}", fill=(255, 255, 255), font=font_body)
                draw.text((50, 180), f"🟢 Wins: {wins}", fill=(0, 255, 100), font=font_body)
                draw.text((50, 230), f"🔴 Losses: {losses}", fill=(255, 75, 75), font=font_body)
                draw.text((50, 280), f"🎯 Accuracy / Win Rate: {win_rate}%", fill=(255, 200, 0), font=font_body)
                
                draw.line([(50, 330), (750, 330)], fill=(51, 65, 85), width=2)
                draw.text((50, 360), f"💰 Net Profit: ${profit}", fill=(0, 255, 150), font=font_title)

                # Footer
                draw.text((50, 440), "⚡ Official Trading Signals & Results", fill=(148, 163, 184), font=font_body)

                # Save Image Locally inside Vercel temp folder
                image_path = "/tmp/pnl_card.png"
                image.save(image_path)

                # Send Photo to Telegram
                with open(image_path, "rb") as photo:
                    files = {"photo": photo}
                    payload = {"chat_id": chat_id, "caption": "🔥 **Your Daily P&L Card is Ready!**", "parse_mode": "Markdown"}
                    requests.post(f"{TELEGRAM_API}/sendPhoto", data=payload, files=files)

            except Exception as e:
                send_message(chat_id, f"❌ Error: {str(e)}")

    return "OK", 200

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)
