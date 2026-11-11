import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "sales_management")

if not MONGODB_URI or not MONGODB_DATABASE:
    raise ValueError("MONGODB_URI and MONGODB_DATABASE must be set")

class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DATABASE]

    def check_connection(self):
        self.client.admin.command("ping")
        return True

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close_connection(self):
        self.client.close()
