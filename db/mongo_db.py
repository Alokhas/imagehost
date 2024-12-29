import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = os.getenv('MONGODB_URL', 'your_mongodb_url')

class MongoDB:
    def __init__(self, url):
        self.client = AsyncIOMotorClient(url)
        self.db = self.client['imagehost_db']  # Database for storing image links
        self.uploads_collection = self.db['uploads']  # Collection for uploads

    async def insert_upload(self, file_url):
        """Insert uploaded file URL into the database."""
        try:
            await self.uploads_collection.insert_one({"file_url": file_url})
        except Exception as e:
            print(f"Error inserting upload into MongoDB: {e}")

    async def get_all_uploads(self):
        """Get all uploaded file URLs from the database."""
        try:
            return await self.uploads_collection.find({}, {"_id": 0, "file_url": 1}).to_list(length=None)
        except Exception as e:
            print(f"Error fetching uploads: {e}")
            return []

    async def count_uploads(self):
        """Get the total count of uploads."""
        try:
            return await self.uploads_collection.count_documents({})
        except Exception as e:
            print(f"Error counting uploads: {e}")
            return 0

async def connect_to_mongodb():
    """Connect to MongoDB and return the MongoDB instance."""
    return MongoDB(MONGODB_URL)


mongo_db = MongoDB(MONGODB_URL)
