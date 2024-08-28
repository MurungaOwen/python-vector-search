from utils.db import MongoDb
from utils.huggingface import generate_embedding
import json
import gradio as gr


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

    return list(results)

def search_interface(product_query: str):
    """Interface to search for products and display them"""
    related_products = get_related_products(product_query)
    if not related_products:
        return "No related products found."
    return "\n\n".join([f"Related product: {doc.get('name', 'No Name')}\nDescription: {doc.get('description', 'No Description')}" for doc in related_products])


if __name__ == "__main__":
    # add_data()
    # store_embeddings()
    
    interface = gr.Interface(
        fn=search_interface, 
        inputs="text", 
        outputs="text", 
        title="Related Product Search",
        description="Search for related products using an AI-powered vector search"
    )

    interface.launch(server_name="0.0.0.0", share=True)
    products_db.close_connection()

