from utils.embedding import get_embeddings
from utils.similarity import cosine_similarity
from models.document import Document
from models.chunk import DocumentChunk

def retrieve_relevant_chunks(question, db):
    question_vector = get_embeddings(question)

    chunks = db.query(DocumentChunk).all()

    results = []

    for chunk in chunks:
        chunk_vector = eval(chunk.embedding) #tempo
        score = cosine_similarity(question_vector, chunk_vector)

        results.append({
            "content": chunk.content,
            "score": score
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    top_chunks = results[:3]

    return top_chunks