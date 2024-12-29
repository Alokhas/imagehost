import os
import httpx
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import Message
from httpx import HTTPStatusError
from db.mongo_db import mongo_db

async def upload_file_to_envs(file_content: BytesIO, file_name="image.jpg"):
    async with httpx.AsyncClient() as client:
        files = {'file': (file_name, file_content.getvalue(), 'image/jpeg')}
        try:
            response = await client.post('https://envs.sh', files=files)
            response.raise_for_status()
            return response.text.strip()
        except HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

@Client.on_message(filters.photo)
async def handle_photo(client: Client, message: Message):
    photo_file_path = await message.download()
    with open(photo_file_path, 'rb') as f:
        photo_bytes = BytesIO(f.read())

    temp_message = await message.reply("Uploading your image to envs.sh...")

    response_data = await upload_file_to_envs(photo_bytes)

    if response_data:
        formatted_link = f"Your image uploaded successfully:\n\nLink: {response_data}\nClick to copy: `{response_data}`"
        await temp_message.edit(formatted_link)

        if mongo_db:
            await mongo_db.insert_upload(response_data)
    else:
        await temp_message.edit("Failed to upload the image. Please try again.")

    os.remove(photo_file_path)
