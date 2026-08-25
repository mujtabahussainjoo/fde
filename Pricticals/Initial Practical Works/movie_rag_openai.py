"""Build a Chroma movie knowledge base and answer questions with OpenAI."""

# Task points:
# 1. Load and split text data from files.
# 2. Store the text chunks in a Chroma collection with metadata.
# 3. Set up an OpenAI client for generating completions.
# 4. Retrieve relevant chunks from the collection for a user query.
# 5. Assemble a prompt using the user's question and search results.
# 6. Use the prompt to get an informed answer from the language model.

import os
from pathlib import Path

import chromadb
from openai import OpenAI

try:
    # Current LangChain installations use the standalone splitter package.
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    # Fallback for older LangChain installations.
    from langchain.text_splitter import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).parent
COLLECTION_NAME = "prompt_practice"
DEFAULT_MODEL = "gpt-4o-mini"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

MOVIE_DOCUMENTS = [
    {
        "file": "2001.txt",
        "url": "https://en.wikipedia.org/wiki/2001:_A_Space_Odyssey",
        "title": "2001: A Space Odyssey",
    },
    {
        "file": "Her.txt",
        "url": "https://en.wikipedia.org/wiki/Her_(film)",
        "title": "Her",
    },
    {
        "file": "WALLE.txt",
        "url": "https://en.wikipedia.org/wiki/WALL-E",
        "title": "WALL-E",
    },
]


def load_movie_chunks():
    """Read each movie file and return its overlapping text chunks with metadata."""
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", "? ", "! "],
        chunk_size=2000,
        chunk_overlap=400,
    )
    missing_files = []
    chunks_to_store = []

    for movie in MOVIE_DOCUMENTS:
        file_path = BASE_DIR / movie["file"]
        if not file_path.exists():
            missing_files.append(movie["file"])
            continue

        content = file_path.read_text(encoding="utf-8")
        chunks = text_splitter.create_documents([content])

        for chun_kindex, chunk in enumerate(chunks):
            chunks_to_store.append(
                {
                    "id": f"{movie['title']}-{chunk_index}",
                    "document": chunk.page_content,
                    "metadata": {
                        "chunk_idx": chunk_index,
                        "url": movie["url"],
                        "title": movie["title"],
                    },
                }
            )

    if missing_files:
        missing = ", ".join(missing_files)
        raise FileNotFoundError(
            f"Missing movie files: {missing}. "
            f"Place them beside {Path(__file__).name}."
        )

    if not chunks_to_store:
        raise ValueError("No text chunks were created.")

    return chunks_to_store


def build_collection(chunks):
    """Create an in-memory Chroma collection and store the movie chunks."""
    # EphemeralClient keeps this practice database in memory for one run.
    chroma_client = chromadb.EphemeralClient()
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["document"] for chunk in chunks],
        # Chroma expects metadatas as a list containing one dictionary per document.
        metadatas=[chunk["metadata"] for chunk in chunks],
    )
    return collection


def get_completion(client, user_prompt, system_prompt, model=DEFAULT_MODEL):
    """Send a prompt to OpenAI and return the generated answer text."""
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return completion.choices[0].message.content


def select_groq_model(client):
    """Return an explicit Groq model or discover one available to the key."""
    configured_model = os.getenv("GROQ_MODEL")
    if configured_model:
        return configured_model

    preferred_models = [
        "openai/gpt-oss-20b",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
    ]
    available_models = {model.id for model in client.models.list().data}

    for model in preferred_models:
        if model in available_models:
            return model

    raise RuntimeError(
        "No supported Groq chat model is available for this API key. "
        "Run `curl https://api.groq.com/openai/v1/models` with your key, "
        "then set GROQ_MODEL to an available model ID."
    )


def make_rag_prompt(query, result_str, include_sources=False):
    """Combine the question and retrieved context into an answer prompt."""
    source_instruction = ""
    if include_sources:
        source_instruction = (
            "At the end of your answer, cite the URL of the search result your "
            "answer draws from. Use this format: <answer>. Source: <URL>\n"
        )

    return f"""Instructions:
Your task is to answer the user question using the search results below.
Use only useful information from the results and do not invent unsupported facts.
{source_instruction}
User question:
{query}

Search Results:
{result_str}

Your answer:
"""


def get_rag_completion(
    openai_client,
    collection,
    query,
    n_results=3,
    model=DEFAULT_MODEL,
    include_sources=False,
):
    """Retrieve context, build a RAG prompt, and ask the language model."""
    search_results = collection.query(query_texts=[query], n_results=n_results)
    result_parts = []

    for document, metadata in zip(
        search_results["documents"][0], search_results["metadatas"][0]
    ):
        # Include the title and URL so the model can identify the source.
        result_parts.append(
            f"Title: {metadata['title']}\n"
            f"URL: {metadata['url']}\n"
            f"Content:\n{document}"
        )

    result_str = "\n\n---\n\n".join(result_parts)
    formatted_query = make_rag_prompt(
        query,
        result_str,
        include_sources=include_sources,
    )
    system_prompt = (
        "You are a helpful RAG search assistant who uses retrieved results "
        "to answer user questions accurately."
    )

    print("\n******** RAG prompt ********\n")
    print(formatted_query)
    print("\n*****************************\n")
    return get_completion(
        openai_client,
        formatted_query,
        system_prompt,
        model=model,
    )


def main():
    chunks = load_movie_chunks()
    collection = build_collection(chunks)

    # OpenAI-compatible providers use the same Python client with a different
    # API key, endpoint, and model. Groq is selected when GROQ_API_KEY exists.
    groq_api_key = os.getenv("GROQ_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if groq_api_key:
        openai_client = OpenAI(
            api_key=groq_api_key,
            base_url=os.getenv("GROQ_BASE_URL", GROQ_BASE_URL),
        )
        # Use GROQ_MODEL when set; otherwise discover an available model.
        model = select_groq_model(openai_client)
    elif openai_api_key:
        openai_client = OpenAI(api_key=openai_api_key)
        model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    else:
        raise EnvironmentError(
            "Set GROQ_API_KEY or OPENAI_API_KEY before running this script."
        )

    query = "What was the plot of Spike Jonze's 'Her'?"

    print(f"Stored {len(chunks)} chunks in '{COLLECTION_NAME}'.")
    print(f"Using model: {model}")
    print("\nAnswer without source citation:")
    print(get_rag_completion(openai_client, collection, query, model=model))

    print("\nAnswer with source citation:")
    print(
        get_rag_completion(
            openai_client,
            collection,
            query,
            model=model,
            include_sources=True,
        )
    )


if __name__ == "__main__":
    main()
