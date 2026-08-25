"""Search a company PDF with keyword and semantic similarity search."""

from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from dotenv import load_dotenv
from pypdf import PdfReader

try:
    from groq import Groq
except ImportError:
    Groq = None


SOURCE_PDF = Path(__file__).with_name("Company Doc.pdf")
OCR_PDF = Path(__file__).with_name("Company Doc OCR.pdf")
load_dotenv(Path(__file__).with_name(".env"))
DEFAULT_PDF = OCR_PDF if OCR_PDF.is_file() else SOURCE_PDF
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150
RESULT_COUNT = 3
ANSWER_CONTEXT_COUNT = 1
MAX_ANSWER_WORDS = 150
RETRIEVAL_COUNT = 8
MAX_CONTEXT_WORDS = 600
QUESTIONS_PER_RUN = 3
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_MODEL_CANDIDATES = (
    DEFAULT_GROQ_MODEL,
    "llama-3.1-8b-instant",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
)
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "company",
    "do", "for", "from", "how", "i", "in", "is", "it", "me", "of", "on",
    "or", "the", "this", "to", "what", "when", "where", "which", "who",
    "with", "you", "your",
}


@dataclass(frozen=True)
class PdfChunk:
    chunk_id: str
    page_number: int
    text: str


def extract_pdf_chunks(pdf_path: Path) -> list[PdfChunk]:
    """Extract non-empty, overlapping text chunks while preserving page numbers."""
    reader = PdfReader(str(pdf_path))
    chunks: list[PdfChunk] = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = "\n".join(
            line.strip()
            for line in (page.extract_text() or "").splitlines()
            if line.strip()
        )
        if not page_text:
            continue

        start = 0
        chunk_number = 1
        while start < len(page_text):
            end = min(start + CHUNK_SIZE, len(page_text))
            chunk_text = page_text[start:end].strip()
            if chunk_text:
                chunks.append(
                    PdfChunk(
                        chunk_id=f"page-{page_number}-chunk-{chunk_number}",
                        page_number=page_number,
                        text=chunk_text,
                    )
                )
            if end == len(page_text):
                break
            start = end - CHUNK_OVERLAP
            chunk_number += 1

    if not chunks:
        raise ValueError("No selectable text was found in the PDF.")
    return chunks


def words(text: str) -> set[str]:
    """Return lowercase words for the simple keyword comparison."""
    return set(re.findall(r"[a-z]+", text.lower()))


def content_words(text: str) -> set[str]:
    """Return meaningful words used for dynamic relevance scoring."""
    return words(text) - STOP_WORDS


def keyword_search(question: str, chunks: list[PdfChunk]) -> list[tuple[PdfChunk, int, set[str]]]:
    """Rank PDF chunks by shared words with the question."""
    question_words = content_words(question)
    ranked = []
    for chunk in chunks:
        shared_words = question_words & words(chunk.text)
        ranked.append((chunk, len(shared_words), shared_words))
    return sorted(ranked, key=lambda item: item[1], reverse=True)[:RESULT_COUNT]


def create_collection(chunks: list[PdfChunk]):
    """Create an in-memory Chroma collection containing PDF chunks."""
    client = chromadb.EphemeralClient()
    collection = client.create_collection(
        name="company_pdf",
        configuration={"hnsw": {"space": "cosine"}},
        embedding_function=DefaultEmbeddingFunction(),
    )
    collection.add(
        ids=[chunk.chunk_id for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        metadatas=[{"page": chunk.page_number} for chunk in chunks],
    )
    return collection


def print_keyword_results(question: str, chunks: list[PdfChunk]) -> None:
    print("1. Keyword match:")
    for chunk, score, shared_words in keyword_search(question, chunks):
        if score:
            label = "shared word is" if score == 1 else "shared words are"
            words_text = '", "'.join(sorted(shared_words))
            print(
                f'  Page {chunk.page_number}: {score} {label} "{words_text}"'
            )
        else:
            print(f"  Page {chunk.page_number}: 0 shared words")


def limit_words(text: str, maximum: int = MAX_ANSWER_WORDS) -> str:
    """Limit displayed answer text to a maximum number of words."""
    answer_words = text.split()
    if len(answer_words) <= maximum:
        return text
    return " ".join(answer_words[: maximum - 1]) + " ..."


def select_groq_model(client) -> str:
    """Select a chat model available to the configured Groq account."""
    available_models = {model.id for model in client.models.list().data}
    requested_model = os.getenv("GROQ_MODEL")
    if requested_model in available_models:
        return requested_model
    for model_name in GROQ_MODEL_CANDIDATES:
        if model_name in available_models:
            return model_name
    raise RuntimeError("No supported Groq chat model is available for this account.")


def print_semantic_results(question: str, collection) -> None:
    result = collection.query(query_texts=[question], n_results=collection.count())
    question_words = content_words(question)
    semantic_results = []
    for text, distance, metadata in zip(
        result["documents"][0],
        result["distances"][0],
        result["metadatas"][0],
    ):
        similarity = 1 - distance
        matched_words = question_words & content_words(text)
        lexical_score = len(matched_words) / max(len(question_words), 1)
        combined_score = (0.7 * similarity) + (0.3 * lexical_score)
        semantic_results.append(
            (combined_score, similarity, matched_words, text, metadata)
        )
    semantic_results.sort(key=lambda item: item[0], reverse=True)

    print("2. Semantic and similarity search:")
    for _, similarity, matched_words, text, metadata in semantic_results[:RESULT_COUNT]:
        matched_label = ", ".join(sorted(matched_words)) or "semantic match"
        print(
            f"  Page {metadata['page']} | similarity {similarity:.3f}: "
            f"matched: {matched_label} | {limit_words(text, 40)}"
        )

    context_parts = [
        f"Page {metadata['page']}: {text}"
        for _, _, _, text, metadata in semantic_results
    ]
    context = limit_words(" ".join(context_parts), MAX_CONTEXT_WORDS)

    print("3. Model answer (Groq):")
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY_TEXT")
    if Groq is not None and api_key:
        try:
            client = Groq(api_key=api_key)
            model_name = select_groq_model(client)
            response = client.chat.completions.create(
                model=model_name,
                temperature=0,
                max_tokens=MAX_ANSWER_WORDS * 2,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer only from the supplied PDF context. "
                            "Do not use previous questions or outside knowledge. "
                            "If the context does not contain the answer, say so. "
                            "Return no more than 150 words."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Question: {question}\nContext:\n{context}",
                    },
                ],
            )
            answer = limit_words(response.choices[0].message.content.strip())
            print(f"{GREEN}{answer}{RESET}")
            return
        except Exception as error:
            print(f"Groq answer generation failed: {error}")
            print("Showing retrieved PDF context instead.\n")

    print(f"{GREEN}Model unavailable. Retrieved PDF context:{RESET}")
    fallback = limit_words(
        context or "No relevant text was found in the PDF.", MAX_ANSWER_WORDS
    )
    print(f"{GREEN}{fallback}{RESET}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search a company PDF.")
    parser.add_argument(
        "pdf_path",
        nargs="?",
        type=Path,
        default=DEFAULT_PDF,
        help="Path to a text-based PDF (default: Company Doc.pdf).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.pdf_path.is_file():
        raise FileNotFoundError(f"PDF not found: {args.pdf_path}")

    chunks = extract_pdf_chunks(args.pdf_path)
    collection = create_collection(chunks)

    print(f"Company PDF: {args.pdf_path.name}")
    print(f"Indexed chunks: {len(chunks)}\n")

    print(
        f"Ask {QUESTIONS_PER_RUN} questions about the PDF. "
        "Type 'exit' or 'quit' to stop early.\n"
    )
    question_number = 1
    while question_number <= QUESTIONS_PER_RUN:
        try:
            question = input(
                f"{RED}Question {question_number} of {QUESTIONS_PER_RUN}: {RESET}"
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if question.lower() in {"exit", "quit"}:
            break
        if not question:
            print("Please enter a question.\n")
            continue

        print(f"{RED}{question}{RESET}")
        print_keyword_results(question, chunks)
        print_semantic_results(question, collection)
        print()
        question_number += 1

    if question_number > QUESTIONS_PER_RUN:
        print("Completed all three questions.")


if __name__ == "__main__":
    main()
