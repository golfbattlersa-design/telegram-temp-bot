import logging
import os
from threading import Thread
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# লগিং সেটআপ
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Render Web Service সচল রাখার জন্য ছোট একটি Flask সার্ভার
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is alive and running!"


def run_web():
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)


# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = [
    [InlineKeyboardButton("📧 Temp Mail নিন", callback_data="get_mail")],
    [InlineKeyboardButton("📱 Temp Number (OTP)", callback_data="get_number")],
    [InlineKeyboardButton("⚙️ কাস্টম মেইল", callback_data="custom_mail")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  welcome_text = (
      "🔥 **Welcome to the Fastest Temp Mail & OTP Bot!** 🚀\n\n"
      "পাসওয়ার্ড বা প্রাইভেসি নিয়ে চিন্তা? এখন থেকে যেকোনো সাইটে আনলিমিটেড টেম্প মেইল ও ফ্রি ওটিপি নাম্বার ব্যবহার করুন এক ক্লিকেই! ⚡\n\n"
      "📌 **আমাদের স্পেশাল ফিচারসমূহ:**\n"
      "• 📧 Instant Temp Mail (অটো ইনবক্স রিফ্রেশ)\n"
      "• 📱 Free Virtual Numbers (OTP রিসিভ করার জন্য)\n"
      "• ⚙️ Custom Username Mail Generator\n\n"
      "👇 নিচ থেকে আপনার প্রয়োজনীয় অপশনটি সিলেক্ট করুন:"
  )

  if update.message:
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
  elif update.callback_query:
    query = update.callback_query
    await query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")


# বাটন ক্লিক হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  back_keyboard = [[InlineKeyboardButton("🔙 হোমে ফিরে যান", callback_data="back_home")]]
  reply_markup = InlineKeyboardMarkup(back_keyboard)

  if query.data == "get_mail":
    text = (
        "📧 **আপনার টেম্প মেইল:**\n`user_abc123@tempmail.com`\n\n(এটি কপি করে ব্যবহার করুন)"
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif query.data == "get_number":
    text = (
        "📱 **ফ্রি ভার্চুয়াল নাম্বার লিস্ট:**\n\n১. 🇰🇷 সাউথ কোরিয়া (+82...)\n২. 🇺🇸 মার্কিন যুক্তরাষ্ট্র (+1...)"
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif query.data == "custom_mail":
    text = "⚙️ **কাস্টম মেইল তৈরি:**\n\nআপনার পছন্দের যেকোনো ৬ অক্ষরের নাম লিখে পাঠান।"
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif query.data == "back_home":
    await start(update, context)


def main():
  # আপনার আসল বট টোকেন নিচের কোটেশনের ভেতর বসান:
  TOKEN = "YOUR_BOT_TOKEN_HERE"

  # ব্যাকগ্রাউন্ডে ওয়েব সার্ভার চালু করা
  Thread(target=run_web, daemon=True).start()

  application = ApplicationBuilder().token(TOKEN).build()
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button_handler))

  print("বট সফলভাবে রান হচ্ছে...")
  application.run_polling()


if __name__ == "__main__":
  main()
