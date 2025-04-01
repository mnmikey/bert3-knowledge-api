import openai
import logging

logging.basicConfig(level=logging.INFO)

EMBEDDING_MODEL = "text-embedding-ada-002"

def embed_chunks(chunks):
    if not isinstance(chunks, list) or not all(isinstance(c, str) for c in chunks):
        raise ValueError("Chunks must be a list of strings.")

    logging.info(f"🔹 Sending {len(chunks)} chunks for embedding using model '{EMBEDDING_MODEL}'")

    try:
        response = openai.Embedding.create(
            input=chunks,
            model=EMBEDDING_MODEL
        )
        embeddings = [d["embedding"] for d in response["data"]]
        logging.info(f"✅ Received {len(embeddings)} embeddings.")
        return embeddings
    except openai.error.OpenAIError as e:
        logging.error(f"🛑 OpenAI API error: {e}")
        raise
