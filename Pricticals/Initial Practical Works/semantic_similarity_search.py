"""Split a llama article, store its chunks in Chroma, and search them."""

from pathlib import Path

import chromadb

try:
    # Current LangChain installations use the standalone package.
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    # Compatibility fallback for older LangChain installations.
    from langchain.text_splitter import RecursiveCharacterTextSplitter


SOURCE_FILE = Path(__file__).with_name("Llama_Wikipedia_Cleaned.txt")
COLLECTION_NAME = "llama_chunks"
SOURCE_URL = "https://en.wikipedia.org/wiki/Llama"


def main():
    # Read the article that will become the RAG knowledge base.
    if not SOURCE_FILE.exists():
        raise FileNotFoundError(
            f"Source file not found: {SOURCE_FILE}. "
            "Place Llama_Wikipedia_Cleaned.txt beside this script."
        )

    content = SOURCE_FILE.read_text(encoding="utf-8")

    # Split long text into overlapping chunks so each search result has useful context.
    # The overlap helps preserve meaning when an idea crosses a chunk boundary.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
    )
    chunks = text_splitter.create_documents([content])

    if not chunks:
        raise ValueError(f"No text chunks were created from {SOURCE_FILE}.")

    print("First chunk:")
    print(chunks[0].page_content)

    # Create an in-memory Chroma database. Its data is deleted when the program ends.
    chroma_client = chromadb.EphemeralClient()

    # Create the collection if it does not exist, or reuse it during this run.
    # Chroma automatically creates embeddings because no explicit embeddings are supplied.
    llama_collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
    )

    # Store every chunk with a unique ID and metadata describing its origin.
    for index, chunk in enumerate(chunks):
        llama_collection.add(
            ids=[f"chunk_{index}"],
            documents=[chunk.page_content],
            metadatas=[
                {
                    "source": SOURCE_URL,
                    "chunk_index": index,
                }
            ],
        )

    # Convert the question to an embedding and return the most relevant chunk. What are llamas used for?
    query = input("\nAsk a question about llamas: ").strip()

    if not query:
        raise ValueError("Query cannot be empty.")

    results = llama_collection.query(
        query_texts=[query],
        n_results=1,
    )

    print("\nSearch result:")
    print(results["documents"][0][0])
    print("\nSearch result metadata:")
    print(results["metadatas"][0][0])


if __name__ == "__main__":
    main()
