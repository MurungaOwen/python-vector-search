from utils.db import MongoDb
from utils.huggingface import generate_embedding
import json


products_db = MongoDb("vectorSearch", "products")

def add_data():
    """add our json data to db"""
    with open("products.json", "r") as file:
        data = json.load(file)

    products = data.get("products", [])
    results = products_db.insert_documents(products)
    return results

def store_embeddings():
    """store calculated embedding for each product"""
    for doc in products_db.get_all_documents():
        doc["plot_embedding"] = generate_embedding(doc["description"])
        products_db.update_document({"_id": doc["_id"]}, doc)


def get_related_products(query: str):
    """get products matching the query"""
    results = products_db.collection.aggregate(
        [{
            "$vectorSearch": {
                "queryVector": generate_embedding(query),
                "path": "plot_embedding",
                "numCandidates": 100,
                "limit":4,
                "index": "relatedProducts"
            }}
        ]
    )

    return results

if __name__ == "__main__":
    add_data()
    store_embeddings()
    
    product = input("What do you want to search for: ")
    for result in get_related_products(product):
        print("Related product: {} description: {}".format(result["name"], result["description"]))
    products_db.close_connection()

