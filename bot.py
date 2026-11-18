import logging
import os
import random
import re
from threading import Thread
import requests
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

# লগিং সেটআপ
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Render Web Service সচল রাখার জন্য ফ্লাস্ক সার্ভার
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is alive and running!"


def run_web():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


# সবচেয়ে নির্ভরযোগ্য 1SecMail ডোমেইন তালিকা
DOMAINS = ["1secmail.com", "1secmail.org", "1secmail.net"]


# /start কমান্ড এবং মূল মেনু
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = [
    [InlineKeyboardButton("📧 Temp Mail (Live Inbox)", callback_data="mail_menu")],
    [InlineKeyboardButton("📱 Temp Numbers Hub", callback_data="number_menu")],
    [InlineKeyboardButton("ℹ️ বটের নির্দেশিকা ও সাহায্য", callback_data="help_info")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  welcome_text = (
      "🔥 **Welcome to the Ultimate Temp Mail & OTP Bot!** 🚀\n\n"
      "পাসওয়ার্ড বা প্রাইভেসি নিয়ে চিন্তা? যেকোনো সাইটে রিয়েল টেম্প মেইল ব্যবহার করুন এবং **সরাসরি টেলিগ্রামের ভেতরেই** ইনবক্স ও ওটিপি কোড দেখে নিন! ⚡\n\n"
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
    [InlineKeyboardButton("⚡ ইনস্ট্যান্ট মেইল ও ইনবক্স নিন", callback_data="get_random_mail")],
    [InlineKeyboardButton("⚙️ কাস্টম মেইল তৈরি করুন", callback_data="custom_mail_prompt")],
    [InlineKeyboardButton("🔙 হোমে ফিরে যান", callback_data="back_home")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  text = (
      "📧 **Direct Telegram Inbox Hub:**\n\n"
      "নিচের অপশন থেকে মেইল তৈরি করুন। এরপর ইনবক্স চেক বাটনে ক্লিক করলেই টেলিগ্রামের ভেতরে মেসেজ দেখতে পাবেন!"
  )
  await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")


# নাম্বার মেনু হ্যান্ডলার
async def number_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  keyboard = [
    [InlineKeyboardButton("🇺🇸 United States (+1)", callback_data="num_us"), InlineKeyboardButton("🇰🇷 South Korea (+82)", callback_data="num_kr")],
    [InlineKeyboardButton("🇬🇧 United Kingdom (+44)", callback_data="num_uk"), InlineKeyboardButton("🇨🇦 Canada (+1)", callback_data="num_ca")],
    [InlineKeyboardButton("🔙 হোমে ফিরে যান", callback_data="back_home")],
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)

  text = "📱 **Global Virtual Numbers Hub:**\n\nওটিপি ভেরিফিকেশনের জন্য দেশ সিলেক্ট করুন:"
  await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")


# বাটন ক্লিক হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  await query.answer()

  data = query.data

  if data == "mail_menu":
    await mail_menu_handler(update, context)
  elif data == "number_menu":
    await number_menu_handler(update, context)
  elif data == "back_home":
    await start(update, context)

  elif data == "get_random_mail":
    name = f"user{random.randint(10000, 99999)}"
    domain = random.choice(DOMAINS)
    email = f"{name}@{domain}"

    context.user_data["current_email"] = email
    context.user_data["mail_user"] = name
    context.user_data["mail_domain"] = domain

    keyboard = [
        [InlineKeyboardButton("📥 টেলিগ্রামেই ইনবক্স চেক করুন", callback_data="check_inbox")],
        [InlineKeyboardButton("🔄 নতুন মেইল নিন", callback_data="get_random_mail")],
        [InlineKeyboardButton("🔙 ব্যাকে যান", callback_data="mail_menu")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"📧 **আপনার রিয়েল টেম্প মেইল:**\n`{email}`\n\n"
        f"✅ এই মেইলটি কপি করে যেকোনো সাইটে ব্যবহার করুন। কোড পাঠানোর পর নিচের **'টেলিগ্রামেই ইনবক্স চেক করুন'** বাটনে ক্লিক করলেই ওটিপি দেখতে পাবেন!"
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif data == "check_inbox":
    mail_user = context.user_data.get("mail_user")
    mail_domain = context.user_data.get("mail_domain")

    if not mail_user:
      await query.message.reply_text("⚠️ প্রথমে একটি মেইল তৈরি করুন!")
      return

    api_url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={mail_user}&domain={mail_domain}"
    try:
      # টাইমআউট যুক্ত করা হয়েছে যাতে রিকোয়েস্ট আটকে না থাকে
      response = requests.get(api_url, timeout=10)
      messages = response.json()

      keyboard = [
          [InlineKeyboardButton("📥 আবার ইনবক্স রিফ্রেশ করুন", callback_data="check_inbox")],
          [InlineKeyboardButton("🔙 হোমে ফিরে যান", callback_data="back_home")],
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)

      if not messages:
        text = (
            f"📭 **ইনবক্স খালি!**\n\nআপনার মেইল: `{mail_user}@{mail_domain}`\n"
            f"এখনো কোনো নতুন মেসেজ বা ওটিপি আসেনি। সাইটে কোড পাঠানোর পর রিফ্রেশ করুন।"
        )
      else:
        text = f"📬 **আপনার ইনবক্সে {len(messages)} টি নতুন মেসেজ এসেছে!**\n\n"
        for msg in messages[:3]:
          msg_id = msg.get("id")
          from_sender = msg.get("from")
          subject = msg.get("subject")

          detail_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={mail_user}&domain={mail_domain}&id={msg_id}"
          detail_res = requests.get(detail_url, timeout=10).json()
          body = detail_res.get("textBody", "Content not available")

          text += f"👤 **প্রেরক:** {from_sender}\n📌 **বিষয়:** {subject}\n💬 **টেক্সট/কোড:**\n`{body[:300]}`\n\n-------------------\n"

      await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    except Exception as e:
      logging.error(f"Inbox Error: {e}")
      await query.message.reply_text("❌ এপিআই সার্ভারে সংযোগ স্থাপন করতে সমস্যা হচ্ছে। দয়া করে কয়েক সেকেন্ড পর আবার চেষ্টা করুন।")

  elif data == "custom_mail_prompt":
    context.user_data["waiting_for_custom_mail"] = True
    keyboard = [[InlineKeyboardButton("🔙 ব্যাকে যান", callback_data="mail_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "⚙️ **কাস্টম মেইল তৈরি:**\n\nদয়া করে আপনার পছন্দের নাম চ্যাট বক্সে লিখে পাঠান (যেমন: `myname123`):"
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif data in ["num_us", "num_kr", "num_uk", "num_ca"]:
    keyboard = [[InlineKeyboardButton("🔙 ব্যাকে যান", callback_data="number_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = (
        f"📱 **Virtual Number Hub**\n\nনম্বর: `+1 (800) 555-0199`\n\n✅ অ্যাকাউন্ট ভেরিফিকেশনের জন্য এটি ব্যবহার করতে পারেন।"
    )
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

  elif data == "help_info":
    keyboard = [[InlineKeyboardButton("🔙 হোমে ফিরে যান", callback_data="back_home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "ℹ️ **নির্দেশিকা:** মেইল নিয়ে সাইটে কোড পাঠিয়ে টেলিগ্রামের ভেতরেই ইনবক্স চেক করতে পারবেন।"
    await query.message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")


# কাস্টম মেইল হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if context.user_data.get("waiting_for_custom_mail"):
    text_input = update.message.text.strip()
    clean_name = re.sub(r"[^a-zA-Z0-9]", "", text_input).lower()

    if len(clean_name) < 3:
      await update.message.reply_text("❌ নামের দৈর্ঘ্য অন্তত ৩ অক্ষরের হতে হবে। আবার লিখুন:")
      return

    domain = random.choice(DOMAINS)
    email = f"{clean_name}@{domain}"
    context.user_data["waiting_for_custom_mail"] = False
    context.user_data["current_email"] = email
    context.user_data["mail_user"] = clean_name
    context.user_data["mail_domain"] = domain

    keyboard = [
        [InlineKeyboardButton("📥 টেলিগ্রামেই ইনবক্স চেক করুন", callback_data="check_inbox")],
        [InlineKeyboardButton("🔙 হোমে ফিরে যান", callback_data="back_home")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    response_text = (
        f"🎉 **কাস্টম মেইল তৈরি সফল!**\n\n📧 মেইল: `{email}`\n\n"
        f"✅ সাইটে কোড পাঠিয়ে নিচের বাটনে ক্লিক করলেই টেলিগ্রামের ভেতরে ওটিপি দেখতে পাবেন!"
    )
    await update.message.reply_text(response_text, parse_mode="Markdown")
  else:
    await update.message.reply_text("বট পরিচালনা করতে `/start` কমান্ড দিন।")


def main():
  TOKEN = "9035144010:AAElyjhT1sZsZnSNkKqFIDldj_3VVElCVlQ"

  Thread(target=run_web, daemon=True).start()

  application = ApplicationBuilder().token(TOKEN).build()
  application.add_handler(CommandHandler("start", start))
  application.add_handler(CallbackQueryHandler(button_handler))
  application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

  print("ফিক্সড ইনবক্স এপিআই বট রান হচ্ছে...")
  application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
  main()
