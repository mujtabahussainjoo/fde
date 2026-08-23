# Multi-Source Hybrid RAG

## Goal

Real applications have information in many places. A multi-source RAG system searches several internal sources and can optionally search the live web.

Example internal sources:

- Company documents and financial reports
- Structured product catalogs
- Customer reviews
- Knowledge-base articles

Optional external source:

- Live web search for current news, prices, weather, trends, and recent events

## 1. Why Multi-Source RAG Matters

A single question may need several kinds of evidence:

```text
Question
  -> Company documents
  -> Product data
  -> Customer reviews
  -> Knowledge base
  -> Optional live web search
  -> Combined context
  -> One answer with source labels
```

The user gets one answer, but the application can still show which sources contributed.

## 2. Structured Data as Documents

A spreadsheet row or database record can be converted into a document:

```text
Product: AI Assistant Pro
Price: 49
Category: Software
Rating: 4.7
Users: 12000
```

This allows one vector index to search both normal text and structured records. For exact values, filters or SQL should also be used. Vector search alone is not a replacement for reliable database queries.

## 3. Routing Web Search

Internal retrieval should usually happen first. Add web search when the question contains words such as:

- latest
- current
- recent
- today
- now
- news
- price
- weather
- trends
- updates
- breaking

Keyword routing is simple but imperfect. In production, use a classifier, tool-calling model, or an explicit user option, and validate web results.

## 4. Multi-Source Script

Install packages:

```bash
python3 -m pip install langchain langchain-community langchain-google-genai langchain-text-splitters chromadb sentence-transformers pandas google-search-results --break-system-packages
```

Set keys as needed:

```bash
export GOOGLE_API_KEY="your-gemini-api-key"
export SERPAPI_API_KEY="your-serpapi-key"
```

The web key is optional. Without it, internal search still works.

```python
# This script combines internal documents, product rows, reviews, and
# knowledge-base articles. It adds a web result only for current questions.

import os

import pandas as pd
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


class HybridRAG:
    """Search internal data and optionally add live web results."""

    def __init__(self, vectorstore, llm, web_search=None):
        self.vectorstore = vectorstore
        self.llm = llm
        self.web_search = web_search

    def needs_web_search(self, question):
        """Return True when the wording suggests that current data is needed."""
        current_words = {
            "latest", "current", "recent", "today", "now", "news",
            "price", "weather", "trends", "updates", "breaking",
        }
        question_words = set(question.lower().split())
        return bool(current_words.intersection(question_words))

    def search_internal(self, question):
        """Return labeled internal documents for the question."""
        return self.vectorstore.similarity_search(question, k=4)

    def search_web(self, question):
        """Return one web result when a SerpAPI wrapper is configured."""
        if self.web_search is None:
            return []

        try:
            result = self.web_search.run(question)
            return [
                Document(
                    page_content=result,
                    metadata={"source": "web_search", "type": "web"},
                )
            ]
        except Exception as error:
            # A failed optional web search should not destroy internal RAG.
            print(f"Web search failed: {error}")
            return []

    def answer_question(self, question):
        """Retrieve all useful context and generate a source-aware answer."""
        internal_documents = self.search_internal(question)
        web_documents = (
            self.search_web(question)
            if self.needs_web_search(question)
            else []
        )
        all_documents = internal_documents + web_documents
        context = "\n\n".join(
            "[{source} / {kind}]\n{content}".format(
                source=document.metadata.get("source", "unknown"),
                kind=document.metadata.get("type", "internal"),
                content=document.page_content,
            )
            for document in all_documents
        )

        prompt = (
            "Use only the context below. Clearly separate internal and web "
            "information. If the context is insufficient, say you do not know.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        answer = self.llm.invoke(prompt)
        return answer.content, all_documents


# Step 1: Create examples from four different internal source types.
company_documents = [
    Document(
        page_content="Q4 revenue was 2.4 million dollars.",
        metadata={"source": "finance_report", "type": "company_document"},
    ),
]
reviews = [
    Document(
        page_content="Customers rate AI Assistant Pro highly for its fast replies.",
        metadata={"source": "customer_review_1", "type": "review"},
    ),
]
knowledge_articles = [
    Document(
        page_content="Remote workers must use multi-factor authentication.",
        metadata={"source": "security_article", "type": "knowledge_base"},
    ),
]

# Step 2: Convert structured product rows into searchable documents.
products = pd.DataFrame([
    {"name": "AI Assistant Pro", "price": 49, "rating": 4.7, "users": 12000},
    {"name": "Data Analyzer", "price": 79, "rating": 4.5, "users": 8000},
])
product_documents = [
    Document(
        page_content=(
            f"Product: {row['name']}; Price: {row['price']} dollars; "
            f"Rating: {row['rating']}; Users: {row['users']}"
        ),
        metadata={"source": "product_catalog", "type": "product"},
    )
    for _, row in products.iterrows()
]

# Step 3: Combine and split all internal sources.
all_documents = (
    company_documents + product_documents + reviews + knowledge_articles
)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(all_documents)

# Step 4: Embed and index the unified internal collection.
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="multi_source_rag_demo",
)

# Step 5: Create the answer model.
if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("Set GOOGLE_API_KEY before running this script.")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    max_output_tokens=700,
)

# Step 6: Enable web search only when its optional key is available.
web_search = SerpAPIWrapper() if os.getenv("SERPAPI_API_KEY") else None
hybrid_rag = HybridRAG(vectorstore, llm, web_search)

# Step 7: Ask a question. A word such as "latest" can trigger web search.
question = "What are our top-rated products, and what are the latest AI trends?"
answer, source_documents = hybrid_rag.answer_question(question)
print("Answer:\n", answer)
print("\nSources used:")
for document in source_documents:
    print(
        f"- {document.metadata.get('type', 'unknown')}: "
        f"{document.metadata.get('source', 'unknown')}"
    )
```

## 5. Source Transparency

Group returned documents by `metadata["type"]` and display labels such as:

- Company document
- Product catalog
- Customer review
- Knowledge base
- Web search

This lets a user see whether an answer came from private information, customer opinions, or current public data.

## 6. Important Production Improvements

- Use exact database filters for prices, totals, and counts.
- Store web URLs, dates, and result titles, not only web text.
- Check whether web results are trustworthy and current.
- Keep internal data access permissions during retrieval.
- Prevent prompt injection from documents and web pages.
- Cache repeated searches and rate-limit external APIs.
- Log which sources were retrieved for evaluation.
