# RAG Foundations and Retrieval

## 1. What Is RAG?

**RAG** means **Retrieval-Augmented Generation**.

It joins three simple actions:

1. **Retrieve:** Search useful information from documents or a database.
2. **Augment:** Put the found information into the AI prompt.
3. **Generate:** Ask the language model to write an answer using that information.

```text
User question
    -> Search documents
    -> Select useful text
    -> Add text to the prompt
    -> Generate a grounded answer
```

## 2. Why Use RAG?

- The AI can use private company information.
- The knowledge can be updated without training the model again.
- The answer can be based on a selected collection of documents.
- Source metadata can help people check the answer.
- It can reduce guessing when the prompt tells the model to use only the context.

RAG does not guarantee truth. Bad documents or bad retrieval can still produce a bad answer.

## 3. Important Words

| Word | Simple meaning |
| --- | --- |
| Document | Original information, such as a PDF, article, or database row |
| Chunk | A small part of a document |
| Embedding | Numbers that represent the meaning of text |
| Vector database | Storage that searches embeddings efficiently |
| Retriever | The component that finds relevant chunks |
| LLM | The language model that writes the final answer |
| Metadata | Extra details such as source name, date, or document type |

## 4. Why Split Documents Into Chunks?

Large documents are split because:

- Small pieces are easier to search.
- The model receives focused context.
- Very large prompts can exceed the model context limit.
- Metadata can be attached to every piece.

A common starting point is:

- `chunk_size=500`
- `chunk_overlap=50`

Overlap repeats a small part between neighboring chunks. This helps preserve an idea that crosses a chunk boundary.

## 5. Embeddings and Semantic Search

An embedding changes text into a list of numbers. Texts with similar meanings usually have nearby vectors.

Example:

```text
Question: How can I recover my account?
Document: Steps to reset a forgotten password
```

The words are different, but semantic search can still connect them.

The basic search process is:

1. Split documents into chunks.
2. Create an embedding for every chunk.
3. Store the chunks and embeddings in ChromaDB.
4. Create an embedding for the user question.
5. Compare the question with stored vectors.
6. Return the top `k` closest chunks.

## 6. Beginner Retrieval Script

Install the main packages:

```bash
python3 -m pip install langchain-community langchain-text-splitters chromadb sentence-transformers --break-system-packages
```

The first run may download the embedding model.

```python
# This script teaches the retrieval part of RAG.
# It does not call an LLM yet. It only finds useful document chunks.

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Step 1: Create a small knowledge base.
# In a real application, these documents could come from PDFs, websites,
# database exports, support articles, or uploaded files.
documents = [
    Document(
        page_content=(
            "RAG means Retrieval-Augmented Generation. It searches relevant "
            "documents and gives the results to a language model as context."
        ),
        metadata={"source": "rag_definition", "topic": "RAG"},
    ),
    Document(
        page_content=(
            "Embeddings are numerical representations of meaning. A vector "
            "database stores embeddings and supports similarity search."
        ),
        metadata={"source": "embeddings_guide", "topic": "embeddings"},
    ),
    Document(
        page_content=(
            "ChromaDB is a local vector database that can store document text, "
            "embeddings, and metadata for semantic search."
        ),
        metadata={"source": "chroma_guide", "topic": "vector database"},
    ),
]

# Step 2: Split the documents into searchable pieces.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} searchable chunks.")

# Step 3: Load an embedding model.
# all-MiniLM-L6-v2 is small and useful for learning and local demos.
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Step 4: Store chunks and embeddings in a temporary Chroma collection.
# Ephemeral storage disappears when the program ends.
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="rag_foundations_demo",
)

# Step 5: Search by meaning, not only by matching exact words.
question = "How does a system find useful information before answering?"
results = vectorstore.similarity_search(question, k=2)

# Step 6: Display the context that would later be sent to an LLM.
print(f"\nQuestion: {question}")
print("\nRetrieved context:")
for number, document in enumerate(results, start=1):
    print(f"\n{number}. {document.page_content}")
    print(f"   Source: {document.metadata.get('source', 'unknown')}")
```

## 7. Key Memory Points

- RAG is retrieve, augment, and generate.
- Chunking makes documents easier to search.
- Embeddings represent meaning as numbers.
- A vector database stores and searches those vectors.
- `k` controls how many chunks are returned.
- Metadata makes source tracking possible.
