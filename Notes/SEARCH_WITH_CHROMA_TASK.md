# Search with Chroma

A small practice task for learning embeddings, collections, and semantic search with ChromaDB.

## Prerequisites

Install ChromaDB:

```bash
python3 -m pip install chromadb --break-system-packages
```

Chroma's default embedding function uses the `all-MiniLM-L6-v2` model, which creates embeddings with **384 dimensions**. The first run may download this model.

## Complete Practice Code

Save the following as `search_with_chroma.py` and run it with Python:

```python
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


# Use an in-memory client so the exercise can be run repeatedly.
client = chromadb.EphemeralClient()
embedding_function = DefaultEmbeddingFunction()

# 1. Create an embedding and confirm its size.
custom_text = "Chroma stores text as searchable vectors."
custom_embedding = embedding_function([custom_text])[0]

print("Embedding length:", len(custom_embedding))
assert len(custom_embedding) == 384
print("Confirmed: the embedding has 384 dimensions.")

# 2. Create a collection named my_collection.
my_collection = client.create_collection(
    name="my_collection",
    embedding_function=embedding_function,
)

# 3. Generate embeddings for the documents.
docs = ["document one", "document two", "document three"]
ids = ["id1", "id2", "id3"]
doc_embeddings = embedding_function(docs)

# 4. Add documents, IDs, and embeddings to the collection.
my_collection.add(
    ids=ids,
    documents=docs,
    embeddings=doc_embeddings,
)

# 5. Display the collection contents.
print("\\nmy_collection preview:")
print(my_collection.peek())

# 6. Create a cosine-similarity collection.
cosine_collection = client.create_collection(
    name="cosine_collection",
    configuration={"hnsw": {"space": "cosine"}},
    embedding_function=embedding_function,
)

# 7. Add wildlife and solar-system documents.
cosine_collection.add(
    ids=["id1", "id2"],
    documents=[
        "Big cats such as lions, tigers, and leopards are powerful wild animals.",
        "The solar system contains the Sun, planets, moons, asteroids, and comets.",
    ],
)

# 8. Search for wildlife-related content and return one result.
wildlife_result = cosine_collection.query(
    query_texts=["Animals living in the wild"],
    n_results=1,
)

print("\\nWildlife search result:")
print(wildlife_result["documents"][0][0])

# 9. Add a car document and a polar-region document.
cosine_collection.add(
    ids=["id3", "id4"],
    documents=[
        "The internal combustion engine was a groundbreaking invention "
        "that paved the way for the modern automobile.",
        "The North Pole is among the coldest places on the planet, home to "
        "polar bears, seals, and penguins.",
    ],
)

# 10. Search for the car document without repeating its original wording.
car_result = cosine_collection.query(
    query_texts=["A machine that changed transportation through fuel-powered travel"],
    n_results=1,
)

print("\\nCar-related search result:")
print(car_result["documents"][0][0])
```

## Expected Results

The program should show:

```text
Embedding length: 384
Confirmed: the embedding has 384 dimensions.
```

The wildlife search should return the document about **big cats**. The final search should return the document about the **internal combustion engine**, even though the query does not repeat its original wording.

## What This Task Demonstrates

- An embedding converts text into a numeric vector.
- Chroma collections store documents, IDs, and embeddings.
- `peek()` provides a quick view of stored collection data.
- Cosine similarity compares the meaning of vectors.
- Semantic search can find related content without exact keyword matching.
- The `n_results=1` option returns only the best matching result.

## Important Notes

- Each ID must be unique within a collection.
- The number of IDs, documents, and embeddings must match.
- The embedding model must produce the same vector size for all items in a collection.
- `EphemeralClient()` stores data only while the program is running. Use `chromadb.PersistentClient(path="./chroma_data")` when you want to save the collection locally.
