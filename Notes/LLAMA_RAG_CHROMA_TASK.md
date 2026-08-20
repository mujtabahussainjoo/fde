# Task: Build a Simple Llama RAG Search with Chroma

## Objective

Create a small Retrieval-Augmented Generation (RAG) search workflow that:

- Reads a llama article from a text file.
- Splits the article into smaller overlapping chunks.
- Stores the chunks in ChromaDB.
- Searches the stored content using a natural-language question.
- Returns the most relevant chunk and its source information.

## Required Files

Keep these files in the same directory:

```text
Llama_Wikipedia_Cleaned.txt
llama_rag_chroma_search.py
```

`Llama_Wikipedia_Cleaned.txt` is the knowledge source. It contains information about llama habitats, diet, wool, behavior, and uses.

## Prerequisites

Install the required packages:

```bash
python3 -m pip install chromadb langchain-text-splitters --break-system-packages
```

The script also supports older LangChain installations through a fallback import.

## Steps

### 1. Load the Article

Read `Llama_Wikipedia_Cleaned.txt` using UTF-8 encoding.

The script checks that the file exists before reading it. If it is missing, a helpful error message is displayed.

### 2. Split the Text

Use `RecursiveCharacterTextSplitter` with:

- `chunk_size=1500`: Each chunk can contain up to about 1,500 characters.
- `chunk_overlap=300`: Neighboring chunks share 300 characters.

The overlap helps preserve information when a sentence or idea crosses a chunk boundary.

### 3. Create the Chroma Collection

```python
chroma_client = chromadb.EphemeralClient()
llama_collection = chroma_client.get_or_create_collection(
    name="llama_chunks",
)
```

`EphemeralClient()` creates a temporary in-memory database. The data is removed when the program ends.

The collection named `llama_chunks` stores the article chunks and their embeddings.

### 4. Store the Chunks

For every chunk, store:

- A unique ID such as `chunk_0`.
- The chunk text as a document.
- Metadata containing the source URL and chunk number.

Chroma creates embeddings automatically because the script adds documents without manually supplying embeddings.

### 5. Search the Collection

Search with this question:

```text
What are llamas used for?
```

The query is converted into an embedding. Chroma compares it with the stored chunk embeddings and returns the closest result.

The script requests only one result:

```python
n_results=1
```

### 6. Display the Result

The script prints:

- The most relevant document chunk.
- Its source URL.
- Its chunk index.

## Run the Task

From `/var/www/html/fde`, run:

```bash
python3 llama_rag_chroma_search.py
```

## Expected Result

The returned result should mention that llamas are used for purposes such as:

- Carrying loads across mountain paths.
- Producing wool and fiber products.
- Trekking and farming.
- Animal-assisted activities.
- Guarding groups of sheep or goats.
- Companionship and education.

The metadata should look similar to:

```python
{
    "chunk_index": 0,
    "source": "https://en.wikipedia.org/wiki/Llama"
}
```

## What This Task Demonstrates

- Text can be divided into manageable chunks for search.
- Chunk overlap helps preserve context.
- ChromaDB stores documents and their vector embeddings.
- Metadata identifies where a chunk came from.
- Semantic search finds related meaning, not only exact keywords.
- RAG can search a custom knowledge base without retraining an AI model.

## Important Notes

- `EphemeralClient()` does not permanently save data.
- Each chunk ID must be unique within the collection.
- The source text file must be beside the Python script.
- The file name is case-sensitive.
- Use `PersistentClient(path="./chroma_data")` when you need permanent local storage.
