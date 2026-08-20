# Conversational RAG With Memory

## Goal

Normal RAG treats every question as new. Conversational RAG remembers earlier turns so the user can ask follow-up questions.

Example:

```text
User: What is RAG?
User: How does it work?
```

The second question is incomplete by itself. Memory helps the system understand that **it** means RAG.

## 1. Two Important Stages

Conversational RAG usually has two stages:

1. **Question rewriting:** Use the conversation history to turn a follow-up into a standalone question.
2. **Answering:** Retrieve documents for the rewritten question and generate an answer from the retrieved context.

```text
Question + chat history
        -> Standalone question
        -> Retrieve relevant chunks
        -> Generate grounded answer
        -> Save new turn in memory
```

## 2. Conversation Memory

`ConversationBufferMemory` stores the messages in order.

Important settings in the older LangChain pattern:

- `memory_key="chat_history"`: Name used by the chain.
- `return_messages=True`: Keep human and AI messages as message objects.
- `output_key="answer"`: Save the answer field.

For long conversations, a full buffer can become too large. Consider summarizing old turns or storing only the important facts.

## 3. Conversation Script

Install packages:

```bash
python3 -m pip install langchain langchain-community langchain-google-genai langchain-text-splitters chromadb sentence-transformers --break-system-packages
```

Set the key:

```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

```python
# This script demonstrates follow-up questions with conversational memory.
# It uses the older ConversationalRetrievalChain API because that is the
# pattern shown in the lesson. New LangChain projects may prefer LCEL or
# create_history_aware_retriever for finer control.

import os

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Step 1: Check the secret before creating the model.
if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("Set GOOGLE_API_KEY before running this script.")

# Step 2: Create the knowledge base used by the conversation.
documents = [
    Document(
        page_content=(
            "RAG means Retrieval-Augmented Generation. It retrieves relevant "
            "documents and gives them to a language model as context."
        ),
        metadata={"source": "rag"},
    ),
    Document(
        page_content=(
            "Conversational RAG adds chat history. It can rewrite a follow-up "
            "question into a complete question before searching."
        ),
        metadata={"source": "conversational_rag"},
    ),
    Document(
        page_content=(
            "Conversation buffer memory stores human and AI messages in order. "
            "It is simple, but long histories can use a lot of context space."
        ),
        metadata={"source": "memory"},
    ),
]

# Step 3: Split and index the documents.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
chunks = splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="conversation_rag_demo",
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Step 4: Create Gemini and memory.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.2,
    max_output_tokens=512,
)
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer",
)

# Step 5: Tell the model how to rewrite follow-ups.
condense_prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template=(
        "Rewrite the latest question as a standalone question.\n"
        "Use the chat history to resolve words such as it, this, or they.\n"
        "Do not answer the question.\n\n"
        "Chat history:\n{chat_history}\n\n"
        "Latest question: {question}\n"
        "Standalone question:"
    ),
)

# Step 6: Tell the model how to answer from retrieved context.
answer_prompt = PromptTemplate(
    input_variables=["context", "question", "chat_history"],
    template=(
        "Answer using only the supplied context. If it is not enough, say "
        "you do not know. Keep the answer clear and concise.\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    ),
)

# Step 7: Build the chain that rewrites, retrieves, answers, and remembers.
conversation = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    condense_question_prompt=condense_prompt,
    combine_docs_chain_kwargs={"prompt": answer_prompt},
    return_source_documents=True,
)

# Step 8: Ask several turns. The later questions depend on earlier turns.
questions = [
    "What is RAG?",
    "How does it work?",
    "What is the difference between normal and conversational RAG?",
]

for question in questions:
    result = conversation.invoke({"question": question})
    print(f"\nUser: {question}")
    print(f"Assistant: {result['answer']}")
    print("Sources:", [
        document.metadata.get("source", "unknown")
        for document in result["source_documents"]
    ])
```

## 4. Memory Limits and Safety

- Do not store secrets or unnecessary personal data in chat history.
- Limit history length for long-running chats.
- Clear memory when a new user or topic begins.
- Show sources so users can verify the answer.
- Test pronouns, short follow-ups, corrections, and topic changes.

## 5. Key Memory Points

- Memory gives RAG context across turns.
- A follow-up should be rewritten before retrieval.
- The rewritten question should be standalone.
- The answer still needs document context; memory alone is not evidence.
- Long memory increases cost and may reduce answer quality.
