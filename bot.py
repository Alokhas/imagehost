import os
import time
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from dotenv import load_dotenv
import httpx
from io import BytesIO
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

API_ID = os.getenv('API_ID', 'your_api_id')
API_HASH = os.getenv('API_HASH', 'your_api_hash')
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token')
ADMIN_ID = int(os.getenv('ADMIN_ID', 'your_admin_id'))
MONGODB_URL = os.getenv('MONGODB_URL', 'your_mongodb_url')
LOG_GROUP_ID = -1002395548077
BOT_IMAGE_URL = os.getenv('BOT_IMAGE_URL', 'your_bot_image_url')

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
health_app = Flask(__name__)

client = AsyncIOMotorClient(MONGODB_URL)
db = client['imagehost_db']
uploads_collection = db['uploads']

@health_app.route('/health', methods=['GET'])
def health_check():
    return "Bot is running", 200

def run_flask():
    health_app.run(host="0.0.0.0", port=8080)

Thread(target=run_flask, daemon=True).start()

async def log_new_user(user_id, username):
    message = f"New user 😗\nId: {user_id}\nUsername: {username}\n#new_user"
    try:
        await app.send_message(LOG_GROUP_ID, message)
    except Exception as e:
        print("Error sending log message:", e)

async def upload_file_to_envs(file_content: BytesIO, file_name="image.jpg"):
    async with httpx.AsyncClient() as client:
        files = {'file': (file_name, file_content.getvalue(), 'image/jpeg')}
        try:
            response = await client.post('https://envs.sh', files=files)
            response.raise_for_status()
            return response.text.strip()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

@app.on_message(filters.photo)
async def photo_handler(client: Client, message):
    photo_file_path = await message.download()
    with open(photo_file_path, 'rb') as f:
        photo_bytes = BytesIO(f.read())

    temp_message = await message.reply("Uploading your image to envs.sh...")

    response_data = await upload_file_to_envs(photo_bytes)

    if response_data:
        formatted_link = f"Your image uploaded successfully:\n\nLink: {response_data}\nClick to copy: `{response_data}`"
        await temp_message.edit(formatted_link)

        try:
            await uploads_collection.insert_one({"file_url": response_data})
        except Exception as e:
            print(f"Error inserting upload into MongoDB: {e}")
    else:
        await temp_message.edit("Failed to upload the image. Please try again.")

    os.remove(photo_file_path)

@app.on_message(filters.command("start"))
async def start_command(client: Client, message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"

    user_data = {
        "user_id": user_id,
        "username": username,
    }
    
    try:
        existing_user = await db.users.find_one({"user_id": user_id})
        
        if existing_user is None:
            await db.users.insert_one(user_data)
            print("User data updated:", user_data)
            await log_new_user(user_id, username)
        else:
            print("User already exists in the database:", user_data)

    except Exception as e:
        print("Error updating user data:", e)
    
    buttons = [
        [
            InlineKeyboardButton("Updates🔊", url="https://t.me/Thealphabotz"),
            InlineKeyboardButton("Support🛠️", url="https://t.me/alphabotzchat")
        ],
        [
            InlineKeyboardButton("donate🦺", url="https://t.me/adarsh2626"),
            InlineKeyboardButton("Source", url="https://t.me/alphabotzchat/599")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)  

    await message.reply_photo(
        photo=BOT_IMAGE_URL,
        caption=(
            "Welcome to ImageHost Bot! Send me an image, and I'll upload it for you.\n\n"
            "I can help you host your images and provide you with a shareable link.\n"
            "Feel free to reach out if you have any questions!"
        ),
        reply_markup=reply_markup
    )

@app.on_message(filters.command("help"))
async def help_cmd(client: Client, message):
    buttons = [
        [InlineKeyboardButton("Close", callback_data="close")]
    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply(
        "Here are some commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Get help with commands\n"
        "/stats - View bot statistics (Admin only)\n"
        "/broadcast - Broadcast a message to all users (Admin only)\n"
        "Send me a photo to upload it and I'll provide a shareable link.\n",
        reply_markup=reply_markup
    )

@app.on_message(filters.command("stats") & filters.user(ADMIN_ID))
async def stats_cmd(client: Client, message):
    try:
        total_users = await db.users.count_documents({})
        total_uploads = await uploads_collection.count_documents({})

        await message.reply(
            f"Bot Statistics:\n"
            f"Total Users: {total_users}\n"
            f"Total Uploads: {total_uploads}"
        )
    except Exception as e:
        await message.reply("An error occurred while fetching statistics.")
        print(f"Error fetching stats: {e}")

@app.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast_cmd(client: Client, message):
    if message.reply_to_message:
        reply_message = message.reply_to_message
        content = reply_message.caption if reply_message.caption else reply_message.text
        media = reply_message.photo if reply_message.photo else None
        
        await message.reply("Broadcasting message...")
        
        user_ids = await db.users.find({}, {"user_id": 1}).to_list(length=None)
        user_ids = [user['user_id'] for user in user_ids]

        for user_id in user_ids:
            try:
                if media:
                    await client.send_photo(user_id, media.file_id, caption=content)
                else:
                    await client.send_message(user_id, content)
            except Exception as e:
                print(f"Failed to send message to {user_id}: {e}")

if __name__ == "__main__":
    time.sleep(10)

    retries = 5
    for attempt in range(retries):
        try:
            app.run()
            break
        except Exception as e:
            print(f"Error: {e}. Attempt {attempt + 1} of {retries}")
            time.sleep(5)