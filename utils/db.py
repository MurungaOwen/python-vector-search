"""our mongo db class"""
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config

class MongoDb():
    def __init__(self, db_name: str, collection_name: str):
        # Connection string from environment variable
        self.mongo_uri = config("MONGO_URI")
        self.client = MongoClient(self.mongo_uri, server_api=ServerApi('1'))
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_document(self, document: dict):
        """Insert a single document into the collection"""
        result = self.collection.insert_one(document)
        print(f"Inserted document with ID: {result.inserted_id}")

    def insert_documents(self, documents: list):
        """Insert multiple documents into the collection"""
        result = self.collection.insert_many(documents)
        print(f"Inserted documents with IDs: {result.inserted_ids}")

    def get_all_documents(self):
        """Retrieve all documents from the collection"""
        return list(self.collection.find())

    def get_document_by_id(self, document_id):
        """Retrieve a document by its _id"""
        return self.collection.find_one({"_id": document_id})

    def update_document(self, filter_criteria: dict, update_data: dict):
        """
        Update a single document based on filter criteria.
        :param filter_criteria: A dictionary representing the filter for finding the document
        :param update_data: A dictionary representing the updated values
        """
        result = self.collection.update_one(filter_criteria, {"$set": update_data})
        print(f"Matched {result.matched_count} document(s) and updated {result.modified_count} document(s)")

    def update_documents(self, filter_criteria: dict, update_data: dict):
        """
        Update multiple documents based on filter criteria.
        :param filter_criteria: A dictionary representing the filter for finding documents
        :param update_data: A dictionary representing the updated values
        """
        result = self.collection.update_many(filter_criteria, {"$set": update_data})
        print(f"Matched {result.matched_count} document(s) and updated {result.modified_count} document(s)")

    def close_connection(self):
        """Close the connection to MongoDB"""
        self.client.close()
        print("MongoDB connection closed.")