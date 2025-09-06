from typing import List, Dict, Any
import os
from .mongo import get_collection


def vector_search(
    collection_name: str,
    query_embedding: List[float],
    top_k: int = 8,
    embedding_field: str = "embedding",
    extra_filter: Dict[str, Any] | None = None,
    include_vector_score: bool = True,
) -> List[Dict[str, Any]]:
    """
    Perform a vector search against a MongoDB Atlas collection using $vectorSearch.

    Assumptions:
    - Documents have a field `embedding_field` storing the vector
    - A vector index exists in Atlas; name via MONGO_VECTOR_INDEX_NAME (default 'vector_index')
    """

    collection = get_collection(collection_name)
    index_name = os.getenv("MONGO_VECTOR_INDEX_NAME", "vector_index")

    pipeline: List[Dict[str, Any]] = [
        {
            "$vectorSearch": {
                "index": index_name,
                "path": embedding_field,
                "queryVector": query_embedding,
                "numCandidates": max(50, top_k * 5),
                "limit": top_k,
            }
        }
    ]

    if extra_filter:
        pipeline.append({"$match": extra_filter})

    if include_vector_score:
        pipeline.append({"$set": {"_score": {"$meta": "vectorSearchScore"}}})

    pipeline.append({"$project": {embedding_field: 0, "_id": 0}})

    return list(collection.aggregate(pipeline))


