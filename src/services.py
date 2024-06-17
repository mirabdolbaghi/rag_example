def chunk_text(text, chunk_size, overlap):
    words = text.split()
    for i in range(0, len(words), chunk_size - overlap):
        yield ' '.join(words[i:i + chunk_size])