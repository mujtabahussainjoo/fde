# RAG Lessons: Comparison and Checklist

## 1. Four Lessons in One View

| Lesson | Main purpose | Main new idea |
| --- | --- | --- |
| Foundations | Prepare data for search | Chunks, embeddings, vector database |
| Complete RAG | Generate an answer | Prompt plus LLM plus retrieved context |
| Conversational RAG | Support follow-up questions | Chat history and question rewriting |
| Multi-source RAG | Search many internal and external sources | Source routing and source attribution |

## 2. Recommended Build Order

1. Start with a few clean documents.
2. Split documents into overlapping chunks.
3. Create embeddings.
4. Store chunks in ChromaDB.
5. Test retrieval without an LLM.
6. Add a strict grounded prompt.
7. Return source documents.
8. Add conversation history.
9. Rewrite follow-up questions before retrieval.
10. Add structured data and web search carefully.
11. Measure retrieval and answer quality.

## 3. What Happens During a Request?

### Basic RAG

```text
Question -> Retrieve -> Prompt with context -> Answer
```

### Conversational RAG

```text
Question + history -> Rewrite -> Retrieve -> Answer -> Save history
```

### Multi-source RAG

```text
Question -> Internal search
         -> Optional web search
         -> Merge labeled context
         -> Answer with source details
```

## 4. Common Mistakes

- Sending the entire document instead of useful chunks.
- Using no chunk overlap when ideas cross boundaries.
- Choosing too many chunks and filling the prompt with noise.
- Allowing the model to answer without a clear context rule.
- Forgetting to return or display source metadata.
- Treating vector search as exact arithmetic or database filtering.
- Using old chat history forever without a size limit.
- Calling live web search for every question.
- Trusting web content without checking its date or source.
- Putting API keys directly into source files.
- Ignoring access permissions on private documents.

## 5. Testing Questions

Use questions from several categories:

- **Known answer:** The answer is clearly in one document.
- **Combined answer:** The answer needs two or more sources.
- **Unknown answer:** The answer is not in the knowledge base.
- **Follow-up:** Uses words such as `it`, `that`, or `they`.
- **Current question:** Uses `latest`, `today`, or `current`.
- **Exact value:** Asks for a price, count, or total that should use structured lookup.
- **Conflicting sources:** Two documents contain different values.

For each test, check:

1. Were the right chunks retrieved?
2. Were irrelevant chunks included?
3. Did the answer stay inside the evidence?
4. Were sources shown correctly?
5. Did the system admit uncertainty?
6. Was web search used only when appropriate?

## 6. Short Glossary

- **RAG:** Retrieval-Augmented Generation.
- **Chunking:** Breaking documents into smaller pieces.
- **Embedding:** A numeric representation of meaning.
- **Vector store:** A system that stores and searches embeddings.
- **Retriever:** A search component that returns relevant chunks.
- **Prompt:** Instructions and input sent to the language model.
- **Grounding:** Making an answer depend on supplied evidence.
- **Memory:** Stored conversation history.
- **Question rewriting:** Turning a follow-up into a complete search question.
- **Hybrid search:** Combining internal retrieval with another source, such as the web.

## 7. Final Memory Formula

```text
Good RAG = Good data
         + Good chunks
         + Good embeddings
         + Good retrieval
         + Clear prompt
         + Source checking
```

The language model is only one part of the system. Retrieval quality and source quality are just as important.

## 8. Practical Security Rules

- Keep API keys in environment variables or a secret manager.
- Do not expose private documents to users without authorization.
- Treat retrieved text as data, not as trusted instructions.
- Validate links and web results.
- Remove sensitive data from logs.
- Add timeouts and error handling to external searches.
- Record source IDs so answers can be audited.
