# LLMOps Practicals Roadmap

This roadmap defines practical work for designing, deploying, integrating, and operating LLM and RAG services.

## Practical Index

1. RAG: Semantic Search and Similarity Search
2. RAG Using a Vector Database
3. RAG with n8n
4. MCP Connections and CI/CD Pipelines
5. CI/CD Practicals
6. AWS Lambda Integrations
7. AWS Pipeline Integrations

---

## 1. RAG: Semantic Search and Similarity Search

**Definition:** Semantic search finds content by meaning. Similarity search ranks text or documents by how close their embeddings are to a query embedding.

**Task:** Design a small search workflow that compares keyword search with embedding-based search.

**Steps:**

1. Select a small, clearly scoped document collection.
2. Clean the text and split it into searchable chunks.
3. Choose an embedding model and define the embedding format.
4. Convert documents and sample questions into embeddings.
5. Calculate similarity scores and rank the closest chunks.
6. Compare results with exact keyword matching.
7. Record relevant results, missed results, latency, and limitations.

## 2. RAG Using a Vector Database

**Definition:** A vector database stores embeddings and retrieves records using similarity search. RAG adds retrieved context to an LLM prompt before generating an answer.

**Task:** Plan an end-to-end RAG knowledge-base service.

**Steps:**

1. Define the users, questions, document sources, and access rules.
2. Design ingestion: load, clean, chunk, embed, and store documents.
3. Define metadata such as source, title, owner, version, and timestamp.
4. Design query retrieval with top-k results and metadata filters.
5. Define a prompt that requires answers to use retrieved context.
6. Plan citations, “I do not know” behavior, and empty-result handling.
7. Evaluate retrieval relevance, answer correctness, citation quality, and latency.

## 3. RAG with n8n

**Definition:** n8n is a visual workflow automation platform that connects APIs, databases, webhooks, and AI services.

**Task:** Design an automated document-to-answer workflow.

**Steps:**

1. Select an input trigger, such as a webhook, upload, or scheduled job.
2. Add validation and a document-processing step.
3. Connect the workflow to an embedding service and vector database.
4. Create a question-answer path that retrieves context and calls an LLM.
5. Add error handling, retries, logging, and notification steps.
6. Protect credentials and define permissions for each connection.
7. Test success, empty data, invalid input, timeout, and duplicate-event cases.

## 4. MCP Connections and CI/CD Pipelines

**Definition:** MCP (Model Context Protocol) standardizes how AI applications connect to tools and resources. CI/CD automates testing and delivery of software changes.

**Task:** Plan a controlled MCP integration and its delivery pipeline.

**Steps:**

1. Identify the tool or resource the model needs and define its input/output contract.
2. Set least-privilege permissions and approval rules for tool calls.
3. Define validation, timeout, audit logging, and failure behavior.
4. Version MCP configuration, prompts, schemas, and application code.
5. Add automated tests for connection, authorization, schema, and unsafe requests.
6. Promote changes through development, staging, and production environments.

## 5. CI/CD Practicals

**Definition:** Continuous Integration validates every change. Continuous Delivery prepares tested changes for release; Continuous Deployment releases them automatically.

**Task:** Define an LLM-aware CI/CD process.

**Steps:**

1. Establish repository structure, branching rules, and environment configuration.
2. Add formatting, linting, unit, integration, and security checks.
3. Test prompts, retrieval quality, model responses, cost, and latency.
4. Build versioned artifacts and publish them to an approved registry.
5. Deploy to staging and run smoke and regression evaluations.
6. Require approval for production and define rollback triggers.
7. Monitor deployment health and record release evidence.

## 6. AWS Lambda Integrations

**Definition:** AWS Lambda runs event-driven functions without managing servers. It is suitable for lightweight API, validation, orchestration, and notification tasks.

**Task:** Design a Lambda integration for an LLM workflow.

**Steps:**

1. Choose an event source such as API Gateway, S3, SQS, or EventBridge.
2. Define the function input, output, timeout, memory, and retry policy.
3. Plan secure access using IAM roles and a secrets manager.
4. Separate fast request handling from long-running work using a queue.
5. Define logs, metrics, tracing, idempotency, and dead-letter handling.
6. Estimate invocation, network, storage, and LLM API costs.
7. Test normal, duplicate, failed, delayed, and unauthorized events.

## 7. AWS Pipeline Integrations

**Definition:** An AWS delivery pipeline builds, tests, scans, approves, and deploys application or infrastructure changes.

**Task:** Plan deployment of the RAG or Lambda service through AWS.

**Steps:**

1. Define source control, build, test, security scan, and artifact stages.
2. Store images and packages in an approved artifact registry.
3. Use separate development, staging, and production environments.
4. Add infrastructure validation and a manual production approval gate.
5. Deploy with versioned configuration and safe rollback support.
6. Add post-deployment smoke tests and operational alerts.
7. Document ownership, audit records, recovery steps, and cost monitoring.

## Completion Standard

Each practical is complete when its design, security cases, failure handling, measurable tests, and reviewable outcome are documented.
