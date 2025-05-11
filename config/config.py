import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


class MongoDB_Client:
    def __init__(self):
        """Initialize the MongoDB connection."""
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self.mongodb_database_name = os.getenv("MONGODB_DATABASE_NAME")
        self.mongodb_session_history_collection = os.getenv(
            "MONGODB_SESSION_HISTORY_COLLECTION"
        )
        self.client = MongoClient(self.mongodb_uri)
        self.model_db = self.client[self.mongodb_database_name]

    def mongodb_collections(self) -> list:
        return self.model_db.list_collection_names()

    def get_collection(self):
        """Retrieve a collection from the database."""
        return self.model_db[self.mongodb_session_history_collection]

    def close_connection(self):
        """Close the MongoDB connection."""
        self.client.close()
