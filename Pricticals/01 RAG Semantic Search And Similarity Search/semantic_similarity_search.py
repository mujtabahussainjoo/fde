"""Compare keyword search with semantic similarity search using ChromaDB."""

from __future__ import annotations

import re
from dataclasses import dataclass

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


@dataclass(frozen=True)
class Document:
    document_id: str
    title: str
    text: str


DOCUMENTS = [
    Document(
        "policy-1",
        "Remote Work",
        "Employees may work remotely up to three days each week with manager approval.",
    ),
    Document(
        "policy-2",
        "Annual Leave",
        "Full-time employees receive twenty paid vacation days every calendar year.",
    ),
    Document(
        "policy-3",
        "Sick Leave",
        "Employees should notify their manager before the workday when they are ill.",
    ),
    Document(
        "policy-4",
        "Learning Budget",
        "Each employee can use up to one thousand dollars per year for approved courses.",
    ),
    Document(
        "policy-5",
        "Travel Expenses",
        "The company reimburses reasonable hotel, transport, and meal costs for business travel.",
    ),
]

QUESTIONS = [
    "How many days can I work from home?",
    "What is my yearly holiday allowance?",
    "Can the company pay for a professional course?",
]


def words(text: str) -> set[str]:
    """Return lowercase words used for the simple keyword comparison."""
    return set(re.findall(r"[a-z]+", text.lower()))


def keyword_search(
    question: str, documents: list[Document]
) -> list[tuple[Document, int, set[str]]]:
    """Rank documents and return the shared words with each document."""
    question_words = words(question)
    ranked = [
        (document, len(shared_words := question_words & words(document.text)), shared_words)
        for document in documents
    ]
    return sorted(ranked, key=lambda item: item[1], reverse=True)


def create_collection():
    """Create an in-memory Chroma collection using cosine distance."""
    client = chromadb.EphemeralClient()
    return client.create_collection(
        name="company_policies",
        configuration={"hnsw": {"space": "cosine"}},
        embedding_function=DefaultEmbeddingFunction(),
    )


def add_documents(collection, documents: list[Document]) -> None:
    collection.add(
        ids=[document.document_id for document in documents],
        documents=[document.text for document in documents],
        metadatas=[{"title": document.title} for document in documents],
    )


def run_semantic_search(collection, question: str, result_count: int = 3):
    return collection.query(query_texts=[question], n_results=result_count)


def main() -> None:
    collection = create_collection()
    add_documents(collection, DOCUMENTS)

    print("RAG Semantic Search and Similarity Search\n")

    for question in QUESTIONS:
        keyword_results = keyword_search(question, DOCUMENTS)[:3]
        semantic_results = run_semantic_search(collection, question)
        result_documents = semantic_results["documents"][0]
        result_distances = semantic_results["distances"][0]

        print(f"Question: {question}")
        print("Keyword search:")
        for document, score, shared_words in keyword_results:
            if score > 0:
                shared_word_label = "shared word is" if score == 1 else "shared words are"
                shared_word_text = '", "'.join(sorted(shared_words))
                print(
                    f'  {document.title}: {score} {shared_word_label} '
                    f'"{shared_word_text}"'
                )
            else:
                print(f"  {document.title}: {score} shared words")

        print("Semantic similarity search:")
        for text, distance in zip(result_documents, result_distances):
            similarity = 1 - distance
            print(f"  {text} | similarity: {similarity:.3f}")
        print()


if __name__ == "__main__":
    main()
