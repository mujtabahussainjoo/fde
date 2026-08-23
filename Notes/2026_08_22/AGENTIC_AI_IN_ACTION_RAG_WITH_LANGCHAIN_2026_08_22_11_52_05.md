# Agentic AI in Action: RAG with LangChain

**Date and time:** 2026-08-22 11:52:05

## 1. What Is RAG?

**RAG** means **Retrieval-Augmented Generation**.

RAG helps an LLM answer questions using relevant information retrieved from documents, databases, websites, or other trusted sources.

```text
Question -> Find relevant information -> Add it to the prompt -> Generate answer
```

**Simple example:** Instead of asking an LLM to guess a company's leave policy, RAG finds the policy document and asks the LLM to answer using that document.

**Memory shortcut:** **RAG = retrieve facts, then generate an answer.**

## 2. Why Do We Need RAG?

Standalone LLMs can:

- Hallucinate or invent facts.
- Use outdated training information.
- Create nonexistent citations or statistics.
- Lack access to private company data.
- Give confident answers without evidence.

RAG reduces these problems by retrieving current and relevant information at answer time.

### RAG Compared with Other Methods

| Method | Main purpose | Limitation |
| --- | --- | --- |
| **Prompt engineering** | Improves instructions and response style | Does not add new factual knowledge |
| **Fine-tuning** | Teaches a model patterns from new training data | Expensive, slow, and not automatically current |
| **Manual verification** | Humans check the answer | Slow and difficult to scale |
| **RAG** | Retrieves trusted information before generation | Depends on good data and retrieval |

**Key idea:** RAG combines the LLM's language ability with external evidence.

## 3. Anatomy of a RAG Pipeline

A RAG system has two main phases: **prepare the knowledge** and **answer the question**.

### Phase A: Prepare the Knowledge Base

```text
Documents -> Chunking -> Embeddings -> Vector Store
```

### Phase B: Answer a Question

```text
Question -> Query Embedding -> Retriever -> Relevant Chunks -> LLM -> Grounded Answer
```

### Complete Flow

1. Load documents.
2. Split documents into smaller chunks.
3. Convert chunks into embeddings.
4. Store embeddings in a vector database.
5. Convert the user's question into an embedding.
6. Retrieve the most relevant chunks.
7. Add the chunks to a prompt.
8. Ask the LLM to answer using the retrieved context.
9. Return the answer and, when possible, its sources.

**Memory shortcut:** **Split -> Vectorize -> Store -> Retrieve -> Generate.**

## 4. Important RAG Components

### Documents

Documents are the original knowledge sources, such as PDFs, manuals, policies, websites, reviews, or database exports.

### Chunking

**Chunking** splits a long document into smaller pieces that are easier to search.

**Example:** A 100-page manual can be divided into sections of about 500 characters.

A small overlap between chunks helps prevent important information from being lost at a boundary.

- **`chunk_size`:** Target size of each piece.
- **`chunk_overlap`:** Shared text between neighboring pieces.

### Embeddings

**Embeddings** are numerical vectors that represent the meaning of text.

Texts with similar meanings have similar vector positions, even when they use different words.

**Example:** A question asking “How many holidays do I get?” can match a document saying “Employees receive 22 days of annual leave.”

### Vector Store

A **vector store** saves embeddings and supports fast similarity search.

Popular examples include:

- ChromaDB
- FAISS
- Pinecone
- Weaviate

The vector store can also save the original text and metadata, such as document name, department, date, or source type.

### Retriever

A **retriever** finds the chunks most relevant to the question.

The `k` setting controls how many chunks are returned.

```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)
```

### Prompt

The RAG prompt tells the LLM how to use the retrieved context.

A good prompt should:

- Tell the model to answer from the context.
- Tell it to say “I don't know” when the context is insufficient.
- Keep the answer relevant and concise.
- Include placeholders such as `{context}` and `{question}`.

### Generator or LLM

The LLM reads the question and retrieved context, then creates a natural-language answer.

## 5. Retriever Strategies

### Similarity Search

Finds chunks whose embeddings are closest to the question embedding.

**Best for:** General semantic search.

### Maximal Marginal Relevance (MMR)

Finds relevant chunks while reducing repeated or nearly identical results.

**Best for:** Getting diverse information from the knowledge base.

### Hybrid Retrieval

Combines semantic vector search with keyword-based search.

**Best for:** Enterprise data where exact terms, names, codes, and meaning all matter.

**Example:** A legal search can use semantic meaning plus an exact case number or policy code.

## 6. RAG with LangChain

LangChain provides reusable components for each part of RAG:

- Document loaders and `Document` objects
- Text splitters
- Embedding models
- Vector stores
- Retrievers
- Prompt templates
- Retrieval chains
- Conversational retrieval chains
- LLM integrations

This lets developers assemble a RAG system without manually connecting every operation.

### Basic LangChain RAG Idea

```python
question = "What is RAG?"
context = retriever.invoke(question)
answer = llm.invoke(prompt.format(
    context=context,
    question=question
))
```

### RetrievalQA

**RetrievalQA** combines retrieval and question answering for single-turn questions.

```text
Question -> Retrieve documents -> Generate answer
```

### RAG as an Agent Tool

RAG can also be registered as a tool. An agent can decide when it needs to search internal knowledge before answering or acting.

**Example:** A support agent retrieves a product manual before suggesting a repair.

## 7. Building a Basic RAG System

A practical build process is:

1. **Install dependencies:** LangChain, an embedding library, a vector store, and an LLM.
2. **Create or load documents:** Add text and useful metadata.
3. **Split documents:** Use a text splitter with suitable size and overlap.
4. **Create embeddings:** Convert every chunk into a vector.
5. **Create the vector store:** Save chunks, vectors, and metadata.
6. **Configure the retriever:** Choose search type and number of results.
7. **Load the LLM:** Use a model for answer generation.
8. **Create the RAG prompt:** Include context and question fields.
9. **Create the retrieval chain:** Connect retriever, prompt, and LLM.
10. **Test the system:** Inspect retrieved chunks, answers, and sources.

## 8. Source Transparency

A trustworthy RAG system should show which documents influenced the answer.

Useful metadata includes:

- Source name
- Document ID
- Page number
- Department
- Date
- Source type

**Why it matters:** Users can verify the answer, and developers can find retrieval mistakes.

## 9. Conversational RAG

**Conversational RAG** combines RAG with conversation memory.

Basic RAG treats each question independently. Conversational RAG understands follow-up questions using previous messages.

### Example

1. User: “What is RAG?”
2. Assistant explains RAG.
3. User: “How does it work?”
4. The system understands that “it” means RAG.

### Conversational Flow

```text
Chat history + Follow-up question
        -> Reformulate as a complete question
        -> Retrieve relevant documents
        -> Generate grounded answer
        -> Save the new conversation turn
```

### Main Parts

- **Conversation memory:** Stores questions and answers.
- **Question reformulation:** Changes a vague follow-up into a standalone question.
- **Retriever:** Finds context for the reformulated question.
- **Answer prompt:** Uses the context and conversation history.
- **Source documents:** Show where the answer came from.

A conversation buffer can store the complete history, but long histories increase token usage. A windowed or summarized memory can keep the context smaller.

## 10. Multi-Source RAG

**Multi-source RAG** searches several types of data and combines the results into one answer.

Possible sources include:

- Company documents
- Product catalogs
- Customer reviews
- Knowledge-base articles
- Databases
- Live web search

### Multi-Source Flow

```text
Question
   -> Internal documents
   -> Product data
   -> Reviews
   -> Knowledge base
   -> Optional web search
   -> Combine contexts
   -> Generate cited answer
```

A source router can decide whether the question needs only internal data or also current web information.

**Example:**

- “What is our remote-work policy?” -> Internal company documents.
- “What are the latest AI trends?” -> Internal sources plus web search.
- “What do customers say about our most profitable product?” -> Financial data, product catalog, and reviews.

### Why Metadata Helps

Metadata allows the system to group and filter results by source type, date, department, product, or access permission.

## 11. Improving Retrieval Quality

- Choose meaningful chunk sizes.
- Use a small overlap when information may cross boundaries.
- Store useful metadata.
- Tune the number of retrieved chunks.
- Compare similarity, MMR, and hybrid search.
- Filter results by source, date, or user permission.
- Inspect retrieved chunks during testing.
- Use reranking when the first results are not precise enough.
- Keep the prompt focused on retrieved context.
- Return citations or source information.

## 12. Limitations and Safety

RAG improves grounding, but it does not guarantee a correct answer.

Possible problems include:

- The correct information is not in the knowledge base.
- The retriever returns irrelevant chunks.
- Documents are outdated or contradictory.
- Poor chunking loses important context.
- The LLM misreads the retrieved context.
- Sensitive documents are returned to the wrong user.
- Web results may be unreliable or malicious.

### Good Practices

- Keep source documents updated.
- Validate and clean documents before indexing.
- Apply access control before retrieval.
- Tell the model not to guess when evidence is missing.
- Show sources for important answers.
- Log questions, retrieved documents, and outputs.
- Test difficult queries and empty-result cases.
- Monitor retrieval quality and hallucinations.

**Key principle:** RAG grounds an answer in evidence, but the evidence itself must be relevant, current, and trustworthy.

## 13. Complete Example

A company assistant answers: “How does our product compare with current market options?”

1. Search internal product data.
2. Search customer reviews.
3. Detect the word “current” and activate web search.
4. Retrieve recent market information.
5. Combine the internal and web context.
6. Ask the LLM to compare products without guessing.
7. Show the sources used for each part of the answer.

## 14. Final Revision Summary

- **RAG** means Retrieval-Augmented Generation.
- It retrieves relevant external information before generating an answer.
- The basic pipeline is **chunk -> embed -> store -> retrieve -> generate**.
- **Chunking** divides documents into searchable pieces.
- **Embeddings** represent meaning as vectors.
- **Vector stores** save and search those vectors.
- **Retrievers** find relevant context.
- LangChain provides modular RAG components and chains.
- Conversational RAG uses memory to understand follow-up questions.
- Multi-source RAG combines internal data, structured data, reviews, and web results.
- Good RAG systems use metadata, citations, access control, validation, and monitoring.

**One-line memory trick:** RAG helps an LLM **find the right evidence, place it in context, and then write a grounded answer**.
