import os
import time
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums import ParseMode
from dotenv import load_dotenv
import httpx
from io import BytesIO
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

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

UPLOAD_ANIMATIONS = [
    "📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 [▱▱▱▱▱▱▱▱▱▱]",
    "📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 [▰▱▱▱▱▱▱▱▱▱]",
    "📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 [▰▰▱▱▱▱▱▱▱▱]",
    "📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 [▰▰▰▱▱▱▱▱▱▱]",
    "📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 [▰▰▰▰▱▱▱▱▱▱]",
    "📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 [▰▰▰▰▰▱▱▱▱▱]",
    "📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 [▰▰▰▰▰▰▱▱▱▱]",
    "📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 [▰▰▰▰▰▰▰▱▱▱]",
    "📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 [▰▰▰▰▰▰▰▰▱▱]",
    "📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 [▰▰▰▰▰▰▰▰▰▱]",
    "📤 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 [▰▰▰▰▰▰▰▰▰▰]"
]

@health_app.route('/health', methods=['GET'])
def health_check():
    return "Bot is running", 200

def run_flask():
    health_app.run(host="0.0.0.0", port=8080)

Thread(target=run_flask, daemon=True).start()

async def log_new_user(user_id, username):
    message = f"**📱 New User Connected!**\n\n👤 User: {username}\n🆔 ID: `{user_id}`\n\n#new_user"
    try:
        await app.send_message(LOG_GROUP_ID, message, parse_mode=ParseMode.MARKDOWN)
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
async def photo_handler(client: Client, message: Message):
    progress_msg = await message.reply_text("⚡ 𝙸𝚗𝚒𝚝𝚒𝚊𝚕𝚒𝚣𝚒𝚗𝚐 𝚄𝚙𝚕𝚘𝚊𝚍...")
    
    photo_file_path = await message.download()
    with open(photo_file_path, 'rb') as f:
        photo_bytes = BytesIO(f.read())

    for animation in UPLOAD_ANIMATIONS:
        try:
            await progress_msg.edit_text(animation)
            await asyncio.sleep(0.3)
        except Exception:
            pass

    response_data = await upload_file_to_envs(photo_bytes)

    if response_data:
        buttons = [
            [
                InlineKeyboardButton("🔗 Open Link", url=response_data),
                InlineKeyboardButton("📋 Copy Link", callback_data=f"copy_{response_data}")
            ],
            [InlineKeyboardButton("⭐️ Share Link", callback_data=f"share_{response_data}")]
        ]
        
        success_text = (
            "**✨ 𝙸𝚖𝚊𝚐𝚎 𝚄𝚙𝚕𝚘𝚊𝚍𝚎𝚍 𝚂𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢!**\n\n"
            f"🔗 **Link:** `{response_data}`\n"
            "📥 **Click buttons below to interact**"
        )
        
        await progress_msg.edit_text(
            success_text,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
            parse_mode=ParseMode.MARKDOWN
        )

        try:
            await uploads_collection.insert_one({"file_url": response_data})
        except Exception as e:
            print(f"Error inserting upload into MongoDB: {e}")
    else:
        await progress_msg.edit_text(
            "❌ **𝙵𝚊𝚒𝚕𝚎𝚍 𝚝𝚘 𝚞𝚙𝚕𝚘𝚊𝚍 𝚝𝚑𝚎 𝚒𝚖𝚊𝚐𝚎**\n𝙿𝚕𝚎𝚊𝚜𝚎 𝚝𝚛𝚢 𝚊𝚐𝚊𝚒𝚗.",
            parse_mode=ParseMode.MARKDOWN
        )

    os.remove(photo_file_path)

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
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
            await log_new_user(user_id, username)
    except Exception as e:
        print("Error updating user data:", e)
    
    buttons = [
        [
            InlineKeyboardButton("📢 Updates", url="https://t.me/Thealphabotz"),
            InlineKeyboardButton("💬 Support", url="https://t.me/alphabotzchat")
        ],
        [
            InlineKeyboardButton("💝 Donate", url="https://t.me/adarsh2626"),
            InlineKeyboardButton("ℹ️ Help", callback_data="help")
        ]
    ]
    
    welcome_text = (
        "**🌟 Welcome to ImageHost Bot!**\n\n"
        "📸 Send me any image and I'll provide you with:\n"
        "• 🚀 Instant Upload\n"
        "• 🔗 Direct Link\n"
        "• 📱 Beautiful Preview\n\n"
        "**Features:**\n"
        "• 💫 Animated Upload Progress\n"
        "• 🎯 No Web Preview\n"
        "• 🎨 Stylish Interface\n\n"
        "_Select an option below to continue:_"
    )
    
    await message.reply_photo(
        photo=BOT_IMAGE_URL,
        caption=welcome_text,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.MARKDOWN
    )

@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    data = callback_query.data
    
    if data == "help":
        help_text = (
            "**📖 How to use ImageHost Bot:**\n\n"
            "1️⃣ Send any image to the bot\n"
            "2️⃣ Wait for upload animation\n"
            "3️⃣ Get your direct link\n"
            "4️⃣ Use inline buttons to interact\n\n"
            "_Need more help? Contact support!_"
        )
        
        await callback_query.message.edit_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back", callback_data="back")
            ]])
        )
    
    elif data == "back":
        await callback_query.message.delete()
        
    await callback_query.answer()

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
