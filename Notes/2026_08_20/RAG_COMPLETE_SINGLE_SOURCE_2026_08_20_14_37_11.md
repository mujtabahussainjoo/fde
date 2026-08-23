# Complete Single-Source RAG Pipeline

## Goal

This lesson connects retrieval to a language model. The complete flow is:

```text
Documents -> Chunks -> Embeddings -> ChromaDB
                                      |
Question -> Retriever -> Context -> Prompt -> LLM -> Answer
```

The first lesson stopped after retrieval. This lesson adds the prompt and answer generation.

## 1. Main Components

- **Knowledge base:** The information the system is allowed to use.
- **Text splitter:** Breaks long text into smaller chunks.
- **Embedding model:** Converts chunks and questions into vectors.
- **ChromaDB:** Searches for similar chunks.
- **Prompt template:** Tells the model how to use the context.
- **LLM:** Writes the final response.
- **Source documents:** Show which chunks influenced the response.

## 2. Grounding Prompt

A useful beginner prompt should say:

- Use the supplied context.
- Answer the question directly.
- Say that you do not know when the context is insufficient.
- Do not invent facts.
- Keep the answer clear and relevant.

## 3. Complete Script With Gemini

Install packages:

```bash
python3 -m pip install langchain langchain-community langchain-google-genai langchain-text-splitters chromadb sentence-transformers --break-system-packages
```

Before running, set the API key in the shell:

```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

```python
# This script builds a small single-source RAG question-answering system.
# It retrieves local context first and then asks Gemini to answer from it.

import os

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Step 1: Stop early with a clear message when the API key is missing.
if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("Set GOOGLE_API_KEY before running this script.")

# Step 2: Prepare local documents.
documents = [
    Document(
        page_content=(
            "RAG combines retrieval and generation. The retriever finds "
            "relevant text, and the language model uses that text to answer."
        ),
        metadata={"source": "rag_notes"},
    ),
    Document(
        page_content=(
            "Embeddings represent the meaning of text as vectors. ChromaDB "
            "stores those vectors and supports semantic similarity search."
        ),
        metadata={"source": "search_notes"},
    ),
]

# Step 3: Split text so retrieval can return focused context.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
chunks = splitter.split_documents(documents)

# Step 4: Convert chunks into embeddings and index them in ChromaDB.
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="complete_rag_demo",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# Step 5: Create the model used for answer generation.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    max_output_tokens=512,
)

# Step 6: Create instructions that reduce unsupported answers.
qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "Use only the context below to answer the question.\n"
        "If the context does not contain the answer, say you do not know.\n"
        "Do not invent facts. Keep the answer concise.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    ),
)

# Step 7: Join retrieval and generation into one chain.
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": qa_prompt},
)

# Step 8: Run a question and print both the answer and its evidence.
question = "What are embeddings used for in this RAG system?"
result = qa_chain.invoke({"query": question})

print("Answer:")
print(result["result"])
print("\nSources used:")
for document in result["source_documents"]:
    print(f"- {document.metadata.get('source', 'unknown')}")
```

## 4. How One Question Is Processed

1. The user asks a question.
2. ChromaDB searches the indexed chunks.
3. The top chunks become `context`.
4. The prompt combines `context` and `question`.
5. Gemini generates an answer.
6. The application returns the answer and source documents.

## 5. Good Practice

- Use a low temperature for factual answers.
- Return source documents for review.
- Keep retrieved context small and relevant.
- Tell the model what to do when the answer is missing.
- Test questions whose answers are both inside and outside the knowledge base.
- Treat the model output as untrusted until it is checked against sources.
