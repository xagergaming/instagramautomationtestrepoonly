import telebot
import requests
import uuid
import random
import string

# Replace 'YOUR_API_KEY' with your bot's API token
API_KEY = '7263301292:AAEDZfcZDWFsQKxrG5Rw4BPKSDgt6kRLo5o'
bot = telebot.TeleBot(API_KEY)

# Handler for the /start command
@bot.message_handler(commands=['start'])
def start_message(message):
    credits_text = (
        "Credits :-\n"
        "Coded by: @tipsandgamer\n"
        "Published by: @MrRhn\n"
        "Follow on Instagram! https://instagram.com/_ahmed84_"
    )
    bot.send_message(message.chat.id, credits_text)
    bot.send_message(message.chat.id, "Welcome to the Instagram Password Reset Bot!\nUse /help to see available commands.")

# Handler for the /help command
@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = (
        "Here are the available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/credits - Show bot credits\n"
        "/reset - Reset an Instagram password"
    )
    bot.send_message(message.chat.id, help_text)

# Handler for the /credits command
@bot.message_handler(commands=['credits'])
def credits_message(message):
    credits_text = (
        "Instagram Password Reset Bot\n"
        "Coded by: @tipsandgamer\n"
        "Published by: @MrRhn\n"
        "Follow on Instagram! https://instagram.com/_ahmed84_"
    )
    bot.send_message(message.chat.id, credits_text)

# Handler for the /reset command
@bot.message_handler(commands=['reset'])
def reset_password(message):
    bot.send_message(message.chat.id, "Please enter the Instagram username or email address:")
    bot.register_next_step_handler(message, perform_password_reset)

def perform_password_reset(message):
    target = message.text

    # Determine if the input is an email or username
    if "@" in target:
        # If input contains "@", treat it as an email address
        reset_type = "email"
    else:
        # Otherwise, it's a username
        reset_type = "username"

    # Simulating Instagram Password Reset Request
    url = "https://i.instagram.com/api/v1/accounts/send_password_reset/"
    data = {
        "_csrftoken": "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32)),
        reset_type: target,  # Dynamic assignment based on the type
        "guid": uuid.uuid4(),
        "device_id": uuid.uuid4()
    }
    headers = {
        "user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}/{''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase + string.digits, k=16))}; en_GB;)"
    }

    # Send the POST request
    req = requests.post(url, headers=headers, data=data)

    # Handling the response from Instagram
    if "obfuscated_email" in req.text:
        bot.send_message(message.chat.id, f"Password reset link sent to the obfuscated email for {target}.")
    elif req.status_code == 404:
        bot.send_message(message.chat.id, "No user found with that username or email address.")
    else:
        bot.send_message(message.chat.id, f"Instagram API response: {req.text}")

# Start the bot
bot.polling()
