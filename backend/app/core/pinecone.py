from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from app.core.config import settings

# init pinecone
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index("research-agent")

# embedding model (384 dimensions — matches index)
embedder = SentenceTransformer("all-MiniLM-L6-V2")

def store_documents(docs: list[dict], namespace: str):
    """Embed and store documents in Pinecone."""
    vectors = []
    for i, doc in enumerate(docs):
        embedding = embedder.encode(doc["text"]).tolist()
        vectors.append({
            "id": f"{namespace}-{i}",
            "values": embedding,
            "metadata": {
                "text": doc["text"][:1000],
                "url": doc.get("url", "")
            }
        })
        if vectors:
            index.upsert(vectors=vectors, namespace=namespace)

def retrieve_documents(query: str, namespace: str, top_k: int = 5):
    """Retrieve documents from Pinecone."""
    query_embedding = embedder.encode(query).tolist()
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        namespace=namespace,
        include_metadata=True
    )    
    return [
        {
            "text": match.metadata.get("text", ""),
            "url": match.metadata.get("url", ""),
            "score": match.score
        }
        for match in results.matches
    ]    
