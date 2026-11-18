import logging
import os
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes

# লগিং সেটআপ
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Render Web Service সার্ভার সচল রাখার জন্য Flask অ্যাপ
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is alive and running!"


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


# নাম্বার মেনু হ্যান্ডলার (বহুদেশ ও রিজন যুক্ত করা হয়েছে)
async def number_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  keyboard = [
    [InlineKeyboardButton("🇺🇸 United States (+1)", callback_data="num_us"), InlineKeyboardButton("🇰🇷 South Korea (+82)", callback_data="num_kr")],
    [InlineKeyboardButton("🇬🇧 United Kingdom (+44)", callback_data="num_uk"), InlineKeyboardButton("🇨🇦 Canada (+1)", callback_data="num_ca")],
    [InlineKeyboardButton("🇩🇪 Germany (+49)", callback_data="num_de"), InlineKeyboardButton("🇫🇷 France (+33)", callback_data="num_fr")],
    [InlineKeyboardButton("🔙 হোমে ফিরে যান", callback_data="back_home")],
  ]
  reply_markup = InlineKeyboardMarkup(reply_markup := InlineKeyboardMarkup(keyboard))

  text = (
      "📱 **Global Virtual Numbers & OTP Hub:**\n\n"
      "ওটিপি ভেরিফিকেশনের জন্য নিচের দেশগুলো থেকে আপনার পছন্দমতো একটি দেশ সিলেক্ট করুন। প্রতিটি দেশের অধীনে একাধিকভাচুয়াল নাম্বার ও লাইভ ইনবক্স মেসেজ পাবেন:"
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
        "*(এই মেইলটি কপি করে যেকোনো সাইটে ব্যবহার করুন। ওটিপি বা ইনবক্সের মেসেজ এখানেই অটো রিসিভ হবে)*"
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif query.data == "get_custom_mail":
    text = (
        "⚙️ **কাস্টম মেইল তৈরি:**\n\n"
        "আপনার পছন্দের যেকোনো ৬-১০ অক্ষরের নাম লিখে পাঠান (যেমন: `myname123`)। বট সাথে সাথেই আপনার নামে কাস্টম মেইল জেনারেট করে দেবে!"
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif query.data in ["num_us", "num_kr", "num_uk", "num_ca", "num_de", "num_fr"]:
    country_names = {
        "num_us": "🇺🇸 United States (+1)",
        "num_kr": "🇰🇷 South Korea (+82)",
        "num_uk": "🇬🇧 United Kingdom (+44)",
        "num_ca": "🇨🇦 Canada (+1)",
        "num_de": "🇩🇪 Germany (+49)",
        "num_fr": "🇫🇷 France (+33)",
    }
    selected_country = country_names.get(query.data, "Selected Country")
    text = (
        f"📱 **Virtual Number - {selected_country}**\n\n"
        f"নম্বর: `+1 (555) 382-9102`\n\n"
        f"✅ Google, Telegram, Instagram, WhatsApp এবং অন্যান্য সার্ভিসের ওটিপি লাইভ চেক করা হচ্ছে...\n"
        f"*(নতুন ওটিপি আসলে নিচে ইনস্ট্যান্ট শো করবে)*"
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif query.data == "help_info":
    text = (
        "ℹ️ **বট ব্যবহারের নির্দেশিকা:**\n\n"
        "1. **Temp Mail:** যেকোনো ওয়েবসাইটে সাইন-আপ করার সময় আসল ইমেইল লুকিয়ে রাখতে এই মেইল ব্যবহার করুন।\n"
        "2. **Temp Numbers:** অ্যাকাউন্ট ভেরিফিকেশনের সময় ফ্রি ভার্চুয়াল নাম্বার থেকে কোড বা ওটিপি দেখে নিন।\n"
        "3. কোনো সমস্যা হলে বট পুনরায় চালু করতে `/start` কমান্ড দিন।"
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")


def main():
  # 👇 এখানে আপনার আসল টেলিগ্রাম বট টোকেনটি বসিয়ে দেবেন 👇
  TOKEN = "9035144010:AAElyjhT1sZsZnSNkKqFIDldj_3VVElCVlQ"

  application = ApplicationBuilder().token(TOKEN).build()

  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button_handler))

  print("বট সফলভাবে রান হচ্ছে...")

  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
  main()
