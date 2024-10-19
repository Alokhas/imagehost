import os
import time
from pyrogram import Client, filters
from dotenv import load_dotenv
from handlers.photo_handler import handle_photo
from plugins.start import start_handler
from plugins.help import help_handler
from plugins.stats import stats_command
from plugins.broadcast import broadcast_command  # Import your broadcast functionality if needed

load_dotenv()

API_ID = os.getenv('API_ID', 'your_api_id')
API_HASH = os.getenv('API_HASH', 'your_api_hash')
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token')
ADMIN_ID = os.getenv('ADMIN_ID', 'your_admin_id')

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.photo)
async def photo_handler(client: Client, message):
    await handle_photo(client, message)

@app.on_message(filters.command("start"))
async def start_command(client: Client, message):
    await start_handler(client, message)

@app.on_message(filters.command("help"))
async def help_cmd(client: Client, message):
    await help_handler(client, message)

@app.on_message(filters.command("return"))
async def return_command(client: Client, message):
    await start_handler(client, message)

@app.on_message(filters.command("stats") & filters.user(ADMIN_ID))
async def stats_cmd(client: Client, message):
    await stats_command(client, message)

@app.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast_cmd(client: Client, message):
    if message.reply_to_message:
        reply_message = message.reply_to_message
        content = reply_message.caption if reply_message.caption else reply_message.text
        media = reply_message.photo if reply_message.photo else None
        
        await message.reply("Broadcasting message...")  # Confirmation message
        
        # Implement logic to send the broadcast message to user IDs here
        user_ids = []  # List of user IDs to send the broadcast message to

        for user_id in user_ids:
            try:
                if media:
                    await client.send_photo(user_id, media.file_id, caption=content)
                else:
                    await client.send_message(user_id, content)
            except Exception as e:
                print(f"Failed to send message to {user_id}: {e}")

    else:
        await message.reply("Please reply to the message you want to broadcast.")

if __name__ == "__main__":
    # Add a delay before starting your bot
    time.sleep(10)
    
    retries = 5
    for attempt in range(retries):
        try:
            app.run()
            break  # Exit loop if successful
        except Exception as e:
            print(f"Error: {e}. Attempt {attempt + 1} of {retries}")
            time.sleep(5)  # Wait before retrying
