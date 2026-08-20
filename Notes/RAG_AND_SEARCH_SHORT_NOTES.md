# RAG and Search Concepts: Short Notes

## What Is RAG?

**RAG** stands for **Retrieval-Augmented Generation**.

RAG combines:

1. **Retrieval:** Find relevant information from source of information such as documents or a knowledge base.
2. **Augmentation:** Add the retrieved information to the user's prompt.
3. **Generation:** Use an AI model to create an answer based on that information.

### Simple RAG Flow

```text
User question
     |
Search for relevant information
     |
Add the information to the prompt
     |
AI generates an answer
```

RAG helps an AI answer questions using specific, current, or private information.

## RAG vs. Generative AI

### Generative AI Without RAG

- Creates answers from patterns learned during training.
- Does not automatically search a private database or document collection.
- May provide outdated, incomplete, or inaccurate information.
- Works well for general writing, ideas, summaries, and explanations.

### RAG

- Searches a selected knowledge source before generating an answer.
- Can use private documents, company data, and updated information.
- Provides answers that are more relevant to the available source material.
- Can include references or source documents for verification.
- Requires extra systems such as document storage, search, and retrieval.

### Advantages of RAG

- Uses current information without retraining the AI model.
- Helps answer questions about private or specialized data.
- Can reduce hallucinations by providing supporting context.
- Makes it easier to update the knowledge base.
- Can improve the accuracy and relevance of answers.

### Limitations of RAG

- Poor search results can lead to poor answers.
- The retrieved information may be incomplete or incorrect.
- Large documents may exceed the model's context limit.
- Requires document processing, storage, and search infrastructure.
- Adds extra time and cost to the response.
- The AI may still misunderstand or incorrectly use the retrieved content.

## What Is Semantic Search?

**Semantic search** finds information based on meaning and intent, not only exact keywords.

For example, a search for:

```text
How can I reset my password?
```

may also find a document titled:

```text
Steps to recover account access
```

The words are different, but the meaning is similar.

## What Is an Embedding?

An **embedding** is a list of numbers that represents the meaning of text, images, or other data.

- Similar meanings produce similar numerical representations.
- Embeddings allow computers to compare the meaning of data.
- Text is usually divided into smaller sections called chunks before embedding.
- Embeddings are stored in a vector database for fast searching.

### Example: Similar Sentences

These sentences have similar meanings, so their embeddings are close:

```text
"I love playing football."
[0.82, 0.14, 0.67, 0.91]

"Football is my favorite sport."
[0.80, 0.16, 0.65, 0.89]
```

These are simplified examples. Real embeddings usually contain hundreds or thousands of numbers.

### Example: Document Search

A document may be split into smaller chunks:

```text
Chunk 1: "Users can reset their password from the account settings page."
Chunk 2: "The application supports payments through credit cards."
Chunk 3: "Reports can be downloaded as PDF files."
```

- Each chunk is converted into an embedding.
- The user's question is also converted into an embedding.
- The system compares the question embedding with the stored chunk embeddings.
- The system selects the most similar chunk as relevant information.

When the user asks:

> How do I change my password?

The system selects **Chunk 1** because its meaning is closest to the question.

## What Is Similarity Search?

**Similarity search** compares a query embedding with stored embeddings and returns the most similar results.

### Basic Process

1. Convert documents into embeddings.
2. Store the embeddings in a vector database.
3. Convert the user's question into an embedding.
4. Compare the question with the stored embeddings.
5. Return the most relevant document chunks.

### Example: Finding the Most Similar Chunk

Suppose the user's question is:

```text
How do I change my password?
```

The question and document chunks are converted into simplified embeddings:

```text
Question: [0.80, 0.20, 0.70]

Chunk 1:  [0.78, 0.22, 0.68]  # Password settings
Chunk 2:  [0.15, 0.90, 0.25]  # Credit card payments
Chunk 3:  [0.30, 0.10, 0.85]  # PDF reports
```

Chunk 1 is most similar to the question, so the system retrieves it and gives it to the AI as context. The AI can then answer that the password can be changed from the account settings page.

The numbers above are simplified for explanation. Real embeddings usually contain many more dimensions.

Common similarity measures include:

- **Cosine similarity:** Compares the direction of two vectors.
- **Euclidean distance:** Measures the distance between two vectors.
- **Dot product:** Compares the relationship between vector values.

For example, with a query vector `[1, 0]` and two stored vectors:

```text
Stored vector A: [0.9, 0.1]
Stored vector B: [0.1, 0.9]
```

Vector A is more similar to the query because it points in nearly the same direction. Depending on the selected measure, the system calculates a similarity score or distance and ranks the results. The highest similarity score, or the lowest distance, is considered the best match.

## How These Concepts Work Together

```text
Documents -> Chunks -> Embeddings -> Vector database
                                         |
User question -> Query embedding -> Similarity search
                                         |
                              Relevant context for the AI
                                         |
                                  Generated answer
```

## Key Takeaways

- Generative AI creates content from learned patterns.
- RAG retrieves useful information before generating an answer.
- Semantic search looks for meaning rather than exact words.
- Embeddings represent meaning as numbers.
- Similarity search finds embeddings that are closest to a query.
- RAG quality depends heavily on the quality of the documents and search results.
## Steps To Install chromadb
- python3 -m pip install chromadb --break-system-packages
- python3 -m pip show chromadb