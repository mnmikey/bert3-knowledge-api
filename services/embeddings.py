import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_chunks(chunks):
    response = openai.Embedding.create(
        input=chunks,
        model="text-embedding-3-small"
    )
    return [d["embedding"] for d in response["data"]]
