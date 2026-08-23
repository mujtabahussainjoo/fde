# Retrieval-Augmented Generation (RAG)

## Anatomy of a RAG Pipeline

```mermaid
flowchart LR
    A[Documents] --> B[Chunking]
    B --> C[Embeddings]
    C --> D[(Vector Store)]
    D --> E[Retriever]
    E --> F[LLM]
    F --> G[Grounded Answer]

    classDef source fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef process fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef storage fill:#fff3e0,stroke:#ef6c00,color:#e65100
    classDef output fill:#fce4ec,stroke:#ad1457,color:#880e4f

    class A source
    class B,C,E process
    class D storage
    class F,G output
```

### Pipeline stages

| Stage | Purpose |
| --- | --- |
| **Documents** | Source material such as files, web pages, manuals, or database records. |
| **Chunking** | Splits documents into smaller passages that can be searched effectively. |
| **Embeddings** | Converts each passage into a numerical vector representing its meaning. |
| **Vector Store** | Stores the vectors and their source text for similarity search. |
| **Retriever** | Finds the passages most relevant to the user's question. |
| **LLM** | Uses the question and retrieved passages to generate a grounded response. |

## RAG vs. Fine-Tuning vs. Prompt Engineering

```mermaid
quadrantChart
    title Choosing an approach
    x-axis Lower flexibility --> Higher flexibility
    y-axis Lower factual accuracy --> Higher factual accuracy
    quadrant-1 RAG sweet spot
    quadrant-2 Fine-tuning
    quadrant-3 Prompt engineering
    quadrant-4 Prompt engineering
    Prompt engineering: [0.72, 0.38]
    Fine-tuning: [0.28, 0.62]
    RAG: [0.78, 0.86]
```

| Approach | Primary purpose | Cost | Flexibility | Factual accuracy |
| --- | --- | --- | --- | --- |
| **Prompt engineering** | Improve instructions and phrasing | Low | High | Limited |
| **Fine-tuning** | Teach the model patterns from new examples | High | Low | Moderate |
| **RAG** | Combine retrieved facts with model reasoning | Medium | High | High |

## Query-time flow

```mermaid
sequenceDiagram
    actor User
    participant App as RAG application
    participant Store as Vector store
    participant Model as Language model

    User->>App: Ask a question
    App->>App: Embed the question
    App->>Store: Search for similar chunks
    Store-->>App: Return relevant context
    App->>Model: Send question plus context
    Model-->>App: Generate grounded answer
    App-->>User: Return answer with sources
```
