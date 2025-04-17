import json
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from .models import init_db, get_db, User
from .services import add_user, set_birthday

async def migrate_data(json_file_path: str):
    # Initialize database
    init_db()
    
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        db = next(get_db())
        
        # Migrate user birthdays
        if 'members' in data:
            for member in data['members']:
                try:
                    # Skip users with blank birthdays
                    if member.get('BirthDay') == 'BLANK' or member.get('BirthMonth') == 'BLANK':
                        print(f"Skipping user {member.get('id')} with blank birthday")
                        continue
                    
                    # Create or update user
                    user = db.query(User).filter(User.telegram_id == int(member['id'])).first()
                    if not user:
                        user = add_user(
                            db,
                            int(member['id']),
                            member.get('username'),
                            member.get('first_name'),
                            None,  # last_name not in original data
                            str(member.get('chatId'))
                        )
                    
                    # Set birthday
                    if user:
                        set_birthday(
                            db,
                            int(member['id']),
                            int(member['BirthDay']),
                            int(member['BirthMonth'])
                        )
                        print(f"Migrated birthday for user {member['id']}: {member['BirthDay']}.{member['BirthMonth']}")
                except (ValueError, KeyError) as e:
                    print(f"Error migrating user {member.get('id')}: {e}")
        
        print("Migration completed successfully!")
    
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python -m src.migrate_data path/to/data.json")
        sys.exit(1)
    
    asyncio.run(migrate_data(sys.argv[1])) 