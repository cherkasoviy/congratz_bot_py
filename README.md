# Congratz Bot

A Telegram bot for sending birthday congratulations and managing user birthdays.

## Features

- Birthday tracking and notifications
- Customizable congratulation messages
- Time zone support
- Admin commands for management
- User-friendly interface
- Database storage for persistence

## Requirements

- Python 3.8+
- aiogram 3.3.0
- python-dotenv 1.0.1
- SQLAlchemy 2.0.27
- Alembic 1.13.1
- Pydantic 2.6.1
- psycopg2-binary 2.9.9

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/congratz_bot.git
cd congratz_bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```
BOT_TOKEN=your_telegram_bot_token
ADMIN_USER_ID=your_telegram_user_id
```

## Usage

1. Start the bot:
```bash
python main.py
```

2. In Telegram, use the following commands:
- `/start` - Start the bot and get welcome message
- `/help` - Show available commands
- `/set_birthday` - Set your birthday
- `/my_birthday` - Check your registered birthday
- `/delete_birthday` - Remove your birthday
- `/timezone` - Set your timezone
- `/list_birthdays` - List all registered birthdays (admin only)
- `/broadcast` - Send message to all users (admin only)

## Development

- The project uses SQLAlchemy for database operations
- Configuration is managed through environment variables
- Logging is implemented for debugging and monitoring
- Code follows PEP 8 style guidelines

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## Author

Your Name - [@yourusername](https://github.com/yourusername)

## Acknowledgments

- python-telegram-bot team
- SQLAlchemy team
- All contributors and users 