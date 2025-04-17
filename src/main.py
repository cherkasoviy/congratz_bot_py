import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session

from .models import init_db, get_db
from .services import (
    add_user, set_birthday, get_user, get_todays_birthdays,
    format_birthday_message, get_random_birthday_sticker
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
dp = Dispatcher()

# Initialize database
init_db()

# Admin user ID (from original JS bot)
ADMIN_USER_ID = 34548632

def get_birthday_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Set my birthday 🎂")],
            [KeyboardButton(text="Check my birthday 📅")]
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    db = next(get_db())
    user = get_user(db, message.from_user.id)
    if not user:
        user = add_user(
            db,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            str(message.chat.id)
        )
    
    await message.answer(
        "👋 Welcome to Congratz Bot!\n\n"
        "I'm here to help you celebrate birthdays! 🎉\n"
        "Use the buttons below to manage your birthday.",
        reply_markup=get_birthday_keyboard()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/setbirthday - Set your birthday\n"
        "/checkbirthday - Check your birthday"
    )

@dp.message(lambda message: message.text == "Set my birthday 🎂")
async def set_birthday_handler(message: types.Message):
    await message.answer(
        "Please send your birthday in the format DD.MM\n"
        "For example: 01.01"
    )

@dp.message(lambda message: message.text == "Check my birthday 📅")
async def check_birthday_handler(message: types.Message):
    db = next(get_db())
    user = get_user(db, message.from_user.id)
    
    if user and user.birth_day and user.birth_month:
        await message.answer(
            f"Your birthday is set to: {user.birth_day}.{user.birth_month}"
        )
    else:
        await message.answer(
            "You haven't set your birthday yet. "
            "Use 'Set my birthday 🎂' to set it!"
        )

@dp.message()
async def handle_message(message: types.Message):
    # Register user if not already registered
    db = next(get_db())
    user = get_user(db, message.from_user.id)
    if not user:
        user = add_user(
            db,
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
            str(message.chat.id)
        )
        logging.info(f"New user registered: {user.first_name} (ID: {user.telegram_id})")
    
    # Handle birthday input
    try:
        # Check if the message is in the format DD.MM
        if '.' in message.text and len(message.text.split('.')) == 2:
            day, month = map(int, message.text.split('.'))
            
            # Validate day and month
            if 1 <= day <= 31 and 1 <= month <= 12:
                # Set the birthday
                user = set_birthday(db, message.from_user.id, day, month)
                
                if user:
                    await message.answer(
                        f"Great! I've set your birthday to {day}.{month} 🎉"
                    )
                else:
                    await message.answer(
                        "Sorry, something went wrong. Please try again later."
                    )
    except ValueError:
        # If the message doesn't match the date format, ignore it
        pass
    
    # Admin feature: Forward messages to a specific chat
    if message.from_user.id == ADMIN_USER_ID and message.chat.type == "private":
        admin_chat_id = "-1001048446549"  # From original JS bot
        try:
            await bot.send_message(admin_chat_id, message.text)
            await bot.send_sticker(admin_chat_id, "CAADAgADkAEAAhmGAwABS5c7xXaQRRYC")
        except Exception as e:
            logging.error(f"Failed to forward admin message: {e}")

async def check_birthdays():
    while True:
        db = next(get_db())
        birthdays = get_todays_birthdays(db)
        
        for user in birthdays:
            if user.chat_id:
                message = format_birthday_message(user)
                sticker = get_random_birthday_sticker()
                
                try:
                    await bot.send_message(user.chat_id, message)
                    await bot.send_sticker(user.chat_id, sticker)
                    logging.info(f"Sent birthday message to chat {user.chat_id} for user {user.first_name}")
                except Exception as e:
                    logging.error(f"Failed to send birthday message to chat {user.chat_id}: {e}")
        
        # Wait for 24 hours before checking again
        await asyncio.sleep(24 * 60 * 60)

async def main():
    # Start the birthday checker in the background
    asyncio.create_task(check_birthdays())
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 