"""hugging face usage"""
from decouple import config
from typing import List
import requests as rq

url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
hugging_face_token = config("HF_TOKEN")

def generate_embedding(text: str) -> List[float]:
    """generates a list of numbers in embedding"""
    headers = {
        "Authorization": f"Bearer {hugging_face_token}"
    }
    response = rq.post(url, headers=headers, json={"inputs": text})
    if response.status_code != 200:
        raise ValueError(f"Failed request with {response.status_code}: {response.text}")
    return response.json()


