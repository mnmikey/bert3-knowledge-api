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
