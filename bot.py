import logging
import os
from threading import Thread
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# লগিং সেটআপ
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# ১. Render Web Service সচল রাখার জন্য ফ্লাস্ক সার্ভার
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is alive and running!"


def run_web():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


# /start কমান্ড এবং মূল মেনু
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = [
    [InlineKeyboardButton("📧 Temp Mail (Inbox & Custom)", callback_data="mail_menu")],
    [InlineKeyboardButton("📱 Temp Numbers (OTP & Regions)", callback_data="number_menu")],
    [InlineKeyboardButton("ℹ️ বটের নির্দেশিকা ও সাহায্য", callback_data="help_info")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  welcome_text = (
      "🔥 **Welcome to the Ultimate Temp Mail & OTP Bot!** 🚀\n\n"
      "পাসওয়ার্ড বা প্রাইভেসি নিয়ে চিন্তা? এখন থেকে যেকোনো সাইটে আনলিমিটেড টেম্প মেইল ও বিশ্বের বিভিন্ন দেশের ফ্রি ওটিপি নাম্বার ব্যবহার করুন এক ক্লিকেই! ⚡\n\n"
      "📌 **আমাদের প্রিমিয়াম ফিচারসমূহ:**\n"
      "• 📧 **Multi-Type Temp Mail:** ইনস্ট্যান্ট, কাস্টম এবং প্রিমিয়াম ডোমেইন মেইল।\n"
      "• 📱 **Global OTP Numbers:** যুক্তরাষ্ট্র, কোরিয়া, যুক্তরাজ্য, কানাডা ও জার্মানি সহ ১৫+ দেশের ভার্চুয়াল নাম্বার।\n"
      "• 🛡️ **100% Secure & Fast:** কোনো রেজিস্ট্রেশন ছাড়াই নিরাপদে ব্যবহার করুন।\n\n"
      "👇 নিচ থেকে আপনার প্রয়োজনীয় অপশনটি সিলেক্ট করুন:"
  )

  if update.message:
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
  elif update.callback_query:
    query = update.callback_query
    await query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")


# মেইল মেনু হ্যান্ডলার
async def mail_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  keyboard = [
    [InlineKeyboardButton("⚡ ইনস্ট্যান্ট র‍্যান্ডম মেইল নিন", callback_data="get_random_mail")],
    [InlineKeyboardButton("⚙️ কাস্টম নাম দিয়ে মেইল বানান", callback_data="get_custom_mail")],
    [InlineKeyboardButton("🔙 হোমে ফিরে যান", callback_data="back_home")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  text = (
      "📧 **Temp Mail Varieties:**\n\n"
      "আপনি কোন ধরনের মেইল চাচ্ছেন তা সিলেক্ট করুন:\n"
      "1. **Instant Mail:** এক ক্লিকেই সিস্টেম আপনাকে একটি রেন্ডম মেইল বানিয়ে দেবে।\n"
      "2. **Custom Mail:** আপনার পছন্দের নাম দিয়ে নিজের মতো করে মেইল আইডি তৈরি করতে পারবেন।"
  )
  await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")


# নাম্বার মেনু হ্যান্ডলার
async def number_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  keyboard = [
    [InlineKeyboardButton("🇺🇸 United States (+1)", callback_data="num_us"), InlineKeyboardButton("🇰🇷 South Korea (+82)", callback_data="num_kr")],
    [InlineKeyboardButton("🇬🇧 United Kingdom (+44)", callback_data="num_uk"), InlineKeyboardButton("🇨🇦 Canada (+1)", callback_data="num_ca")],
    [InlineKeyboardButton("🇩🇪 Germany (+49)", callback_data="num_de"), InlineKeyboardButton("🇫🇷 France (+33)", callback_data="num_fr")],
    [InlineKeyboardButton("🔙 হোমে ফিরে যান", callback_data="back_home")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  text = (
      "📱 **Global Virtual Numbers & OTP Hub:**\n\n"
      "ওটিপি ভেরিফিকেশনের জন্য নিচের দেশগুলো থেকে আপনার পছন্দমতো একটি দেশ সিলেক্ট করুন:"
  )
  await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")


# বাটন ক্লিক এবং সাব-মেনু হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  back_keyboard = [[InlineKeyboardButton("🔙 ব্যাকে যান", callback_data="back_home")]]
  reply_markup = InlineKeyboardMarkup(back_keyboard)

  if query.data == "mail_menu":
    await mail_menu_handler(update, context)
  elif query.data == "number_menu":
    await number_menu_handler(update, context)
  elif query.data == "back_home":
    await start(update, context)

  elif query.data == "get_random_mail":
    text = (
        "📧 **আপনার নতুন ইনস্ট্যান্ট মেইল:**\n"
        "`bot_user992@tempmail.com`\n\n"
        "*(এই মেইলটি কপি করে যেকোনো সাইটে ব্যবহার করুন)*"
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif query.data == "get_custom_mail":
    text = (
        "⚙️ **কাস্টম মেইল তৈরি:**\n\n"
        "আপনার পছন্দের যেকোনো ৬-১০ অক্ষরের নাম লিখে পাঠান (যেমন: `myname123`)*"
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif query.data in ["num_us", "num_kr", "num_uk", "num_ca", "num_de", "num_fr"]:
    text = (
        "📱 **Virtual Number Hub**\n\n"
        "নম্বর: `+1 (555) 382-9102`\n\n"
        "✅ Google, Telegram, Instagram এবং অন্যান্য সার্ভিসের ওটিপি লাইভ চেক করা হচ্ছে..."
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif query.data == "help_info":
    text = (
        "ℹ️ **বটের নির্দেশিকা:**\n\n"
        "1. **Temp Mail:** আসল ইমেইল লুকিয়ে রাখতে এই মেইল ব্যবহার করুন।\n"
        "2. **Temp Numbers:** অ্যাকাউন্ট ভেরিফিকেশনের সময় ফ্রি ভার্চুয়াল নাম্বার থেকে ওটিপি দেখে নিন।"
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")


def main():
  # 👇 এখানে আপনার আসল টেলিগ্রাম বট টোকেনটি বসিয়ে দেবেন 👇
  TOKEN = "9035144010:AAElyjhT1sZsZnSNkKqFIDldj_3VVElCVlQ"

  # ২. ব্যাকগ্রাউন্ডে ফ্লাস্ক সার্ভার থ্রেড চালু করা (যাতে রেন্ডার পোর্ট ওপেন পায়)
  Thread(target=run_web, daemon=True).start()

  # ৩. টেলিগ্রাম বট স্টার্ট করা
  application = ApplicationBuilder().token(TOKEN).build()
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button_handler))

  print("বট সফলভাবে পোলিং মোডে রান হচ্ছে...")
  application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
  main()
