# Code Meaning: Company PDF RAG Search

This document explains how `company_pdf_search.py` works.

## 1. Imported Tools

`pypdf` reads the PDF, `chromadb` performs vector search, `python-dotenv` loads `.env`, and `groq` optionally generates answers. The other imports support paths, regular expressions, input, and data structures.

## 2. PDF Selection

The script prefers `Company Doc OCR.pdf` when present and otherwise uses `Company Doc.pdf`.

The `.env` file is loaded from the same folder. It can contain:

```env
GROQ_API_KEY=your_new_key
GROQ_MODEL=optional_model_name
```

## 3. PDF Text Extraction

`extract_pdf_chunks()` reads every PDF page and keeps its page number.

1. Text is extracted from each page.
2. Empty lines are removed.
3. Text is divided into chunks of 900 characters.
4. Each chunk overlaps the previous chunk by 150 characters.
5. Every chunk receives an ID such as `page-7-chunk-1`.

Page numbers show where information was found.

## 4. Keyword Search

`keyword_search()` compares words in the question with words in every PDF chunk.

- Words are converted to lowercase.
- Common words are ignored for relevance scoring.
- Matching words and their count are displayed.
- The top three keyword matches are shown.

Keyword search works best when the question uses the same words as the PDF.

1. Chunks are added and converted into embeddings.
2. The question is embedded and compared using cosine distance.
3. Distance becomes a similarity score; all chunks are ranked before the best three are displayed.

Semantic search can find related meaning even when exact words differ.

## 6. Three-Part Output

For each question, the script displays:

### Part 1: Keyword Match

Shows pages, match counts, and actual shared words.

### Part 2: Semantic and Similarity Search

Shows three pages, scores, matching terms, and short previews.

### Part 3: Model Answer

The retrieved context is sent to Groq. The model must use only the PDF, ignore previous questions, avoid outside information, report missing answers, and return no more than 150 words.

Python applies the word limit again as a safety check.

## 7. Groq Model Selection

The script checks available models through Groq. It uses `GROQ_MODEL` when available, otherwise selects a supported candidate. API failures do not crash the script; retrieved PDF context is used as a fallback.

## 8. User Interaction

The script asks exactly three questions:

```text
Question 1 of 3:
Question 2 of 3:
Question 3 of 3:
```

Users can type `exit` or `quit` to stop early. Empty questions are rejected.

Questions are red; model answers and fallback context are green using ANSI codes.

## 9. Complete Flow

```text
Load .env
  -> Select OCR PDF
  -> Extract pages
  -> Create overlapping chunks
  -> Index chunks in ChromaDB
  -> Read user question
  -> Show keyword matches
  -> Show semantic matches
  -> Send context to Groq
  -> Print answer under 150 words
  -> Repeat for three questions
```

## 10. Run the Script

From this folder, install dependencies once:

```bash
python3 -m pip install -r requirements.txt
```

Then run:

```bash
python3 company_pdf_search.py
```

## 11. Code-by-Code Understanding

### Imports and Configuration

```python
from pathlib import Path
from pypdf import PdfReader
import chromadb
```

These imports provide file paths, PDF reading, and vector search. `load_dotenv()` reads `.env`. The optional `Groq` import allows the script to run even when the Groq package is missing.

### File and Limit Constants

```python
OCR_PDF = Path(__file__).with_name("Company Doc OCR.pdf")
DEFAULT_PDF = OCR_PDF if OCR_PDF.is_file() else SOURCE_PDF
```

The script prefers the OCR PDF because it normally has better text. `CHUNK_SIZE` and `CHUNK_OVERLAP` control splitting. `MAX_ANSWER_WORDS` limits the final answer to 150 words. `QUESTIONS_PER_RUN` limits the session to three questions.

### PDF Chunk Function

```python
reader = PdfReader(str(pdf_path))
```

The function reads each page, removes empty lines, and creates `PdfChunk` objects. Each object stores an ID, page number, and text. Overlap prevents information at a chunk boundary from being lost.

### Keyword Function

```python
shared_words = question_words & words(chunk.text)
```

The ampersand creates a set intersection. The result contains words appearing in both the question and chunk. Results are sorted by match count and the top three are printed.

### Vector Search Function

```python
collection.add(ids=..., documents=..., metadatas=...)
```

ChromaDB embeds and stores every chunk. `collection.query()` embeds the question, calculates cosine distances, and returns all chunks. The script converts distance to similarity and combines it with meaningful-word overlap before displaying the top three.

### Model Answer Function

The retrieved context is sent to Groq with instructions to use only the PDF and ignore previous questions. `temperature=0` makes the response more consistent. `limit_words()` enforces the 150-word limit after generation. If the key, model, or request fails, the script prints limited retrieved context instead of crashing.

### Main Loop

`input()` reads each question independently. Blank input is rejected. `question_number` increases only after a successful search, and the loop ends after three questions or when the user types `exit` or `quit`.
