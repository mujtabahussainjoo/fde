# Practical 1: RAG Semantic Search and Similarity Search

## Task

Design a simple search experiment that finds relevant document content using both:

- **Keyword search:** Matches the exact words in a question.
- **Semantic search:** Finds content with a similar meaning, even when the exact words are different.
- **Similarity search:** Ranks documents by the closeness of their embedding vectors.

Do not build the application yet. First prepare the data, workflow design, and evaluation plan.

## Objective

Understand how embeddings help a RAG system find useful context before an LLM generates an answer.

## Scenario

Create a small knowledge base for one topic, such as:

- Company policies
- Product documentation
- Course notes
- Travel information

A user will ask questions using words that may differ from the document text. The search design should still find the correct content.

## Step-by-Step Work

### Step 1: Prepare Documents

1. Choose one topic.
2. Collect 5 to 10 short documents or text sections.
3. Give each document a title and unique ID.
4. Record the source of every document.

### Step 2: Create Questions

1. Write five user questions about the documents.
2. Use different wording from the source text in at least three questions.
3. Mark the document that should be the correct result for each question.

### Step 3: Design Text Processing

Document how the text will be:

1. Cleaned by removing unnecessary formatting.
2. Split into small, meaningful chunks.
3. Stored with metadata such as title, source, and document ID.

### Step 4: Plan Embeddings

1. Select an embedding model.
2. Explain that the model converts text into numerical vectors.
3. Plan to create vectors for both document chunks and user questions.
4. Select a similarity method, such as cosine similarity.

### Step 5: Compare Search Methods

For every question, compare:

1. The results expected from keyword search.
2. The results expected from semantic similarity search.
3. The ranking of the top three results.
4. Whether the correct document was found.

### Step 6: Evaluate Results

Create a table with these columns:

- Question
- Expected document
- Keyword result
- Semantic result
- Similarity score
- Correct or incorrect
- Notes

Record missed results, irrelevant results, and possible improvements.

## Deliverables

- Document list with sources and IDs.
- Five test questions with expected answers or documents.
- Search workflow diagram or written flow.
- Comparison table for keyword and semantic search.
- Short recommendation explaining which method is better for this scenario.

## Completion Checklist

- [ ] Documents and sources are identified.
- [ ] Questions use both matching and different wording.
- [ ] Chunking and metadata rules are defined.
- [ ] Embedding and similarity methods are documented.
- [ ] Search results are compared and evaluated.
- [ ] Limitations and improvements are recorded.

## Simple Flow

```text
Documents -> Clean -> Chunk -> Embed -> Store
Question -> Embed -> Compare Similarity -> Rank Results
```
