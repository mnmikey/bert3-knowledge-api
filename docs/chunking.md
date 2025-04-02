# 🧠 chunking.py – Token-Aware Text Chunker

This script is a **utility module** for splitting large blocks of raw text into manageable, token-aware chunks for embedding and vectorization.

---

## 🧩 Modules & Structure

```python
def chunk_text(text, max_tokens=500):
    sentences = text.split(". ")
    chunks, current = [], []
    token_count = 0
    for sentence in sentences:
        tokens = sentence.split()
        if token_count + len(tokens) > max_tokens:
            chunks.append(". ".join(current))
            current, token_count = [], 0
        current.append(sentence)
        token_count += len(tokens)
    if current:
        chunks.append(". ".join(current))
    return chunks
```

---

## ⚙️ Runtime Behavior

- Splits full documents based on sentence boundaries (`. `)
- Tracks token count to ensure no chunk exceeds `max_tokens`
- Returns a list of text chunks suitable for embedding

---

## 🔍 Example

Input: A 1500-token document  
Output: ~3 chunks of 500 tokens each

---

## 🏷 Tags & Metadata

- **Type**: Service
- **Purpose**: Token-aware chunk splitting for NLP ingestion
- **Tags**: `nlp`, `tokenization`, `chunking`, `preprocessing`, `service`
