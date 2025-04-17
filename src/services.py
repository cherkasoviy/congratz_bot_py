from datetime import date, datetime
from sqlalchemy.orm import Session
from .models import User
import random
import os

BIRTHDAY_MESSAGES = [
    "🎉 Happy Birthday! 🎂",
    "🎈 Wishing you a fantastic birthday! 🎁",
    "🌟 Happy Birthday! May your day be filled with joy! 🎊",
    "🎂 Happy Birthday! Wishing you all the best! 🎉",
    "🎁 Happy Birthday! Have a wonderful day! 🎈"
]

# Sticker IDs for birthday messages
BIRTHDAY_STICKERS = [
    "CAADAgADkAEAAhmGAwABS5c7xXaQRRYC"  # Original sticker from JS bot
]

def add_user(db: Session, telegram_id: int, username: str = None, 
             first_name: str = None, last_name: str = None, chat_id: str = None) -> User:
    user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        chat_id=chat_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def set_birthday(db: Session, telegram_id: int, birth_day: int, birth_month: int) -> User:
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if user:
        user.birth_day = birth_day
        user.birth_month = birth_month
        db.commit()
        db.refresh(user)
    return user

def get_user(db: Session, telegram_id: int) -> User:
    return db.query(User).filter(User.telegram_id == telegram_id).first()

def get_todays_birthdays(db: Session) -> list[User]:
    today = date.today()
    return db.query(User).filter(
        User.birth_day == today.day,
        User.birth_month == today.month,
        User.is_active == True
    ).all()

def get_random_birthday_message() -> str:
    return random.choice(BIRTHDAY_MESSAGES)

def get_random_birthday_sticker() -> str:
    return random.choice(BIRTHDAY_STICKERS)

def format_birthday_message(user: User) -> str:
    name = user.first_name or user.username or "there"
    username = f"@{user.username}" if user.username else ""
    return f"Воу-воу-воу, говорят сегодня празднует день рождения {name} {username}, поздравления!" 