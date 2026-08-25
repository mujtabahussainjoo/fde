# LLMOps: Deployment, RAG, Safety, and Optimization

**Created:** 2026-08-24 09:53:20

## Course Overview

LLMOps is the practice of deploying, operating, securing, monitoring, and improving large language model applications in production. It combines ML operations, software engineering, data engineering, platform engineering, and governance.

The main goal is to build LLM applications that are reliable, scalable, cost-effective, versioned, and safe for enterprise use.

## 1. LLM Deployment Strategies

The right deployment method depends on privacy, latency, traffic, cost, customization, and available hardware.

### API-Based Models

- Use a hosted model through an API.
- Fastest way to start and avoids managing GPUs.
- Good for prototypes and teams that do not need full infrastructure control.
- Costs are usually based on input and output tokens.
- Requires attention to data privacy, rate limits, vendor availability, and network latency.

### Self-Hosted Models

- Run model inference on your own cloud or on-premises infrastructure.
- Gives more control over data, versions, networking, and customization.
- Requires GPU capacity, deployment skills, scaling, patching, and monitoring.
- Useful for sensitive data, predictable high traffic, or strict customization requirements.

### Containerized Inference Servers

An inference server packages the model behind a standard serving interface. It can manage batching, GPU use, health checks, and multiple requests.

Common choices include vLLM, Hugging Face TGI, NVIDIA Triton, and managed cloud endpoints.

### Hardware Choices

- **GPU:** Best for high-throughput and low-latency inference.
- **CPU:** Useful for small models, low traffic, or development, but usually slower.
- **Specialized accelerators:** Can reduce cost or improve performance when the model and platform support them.
- **Multiple GPUs:** Needed for large models or higher throughput.

## 2. Packaging LLM Pipelines

A deployable LLM package should include all required model behavior, not only the model file.

Track and version:

- Model weights and architecture.
- Tokenizer and tokenizer configuration.
- Prompt templates and system instructions.
- Generation settings, such as temperature and maximum tokens.
- Retrieval code, embedding model, and index version.
- Dependencies, container image, and runtime configuration.
- Evaluation datasets and quality results.

A **model registry** stores approved model versions, metadata, evaluation results, ownership, and deployment status. This supports reproducibility, promotion, rollback, and auditability.

## 3. API and Inference Patterns

### Synchronous API

The client waits for the complete response.

- Simple request and response experience.
- Good for short answers and interactive applications.
- The request can time out if generation takes too long.

### Asynchronous API

The client submits a job and receives a job ID. It checks status or receives a callback later.

- Good for long documents, expensive generation, and large workloads.
- Often uses a queue such as Amazon SQS or a cloud task service.
- Supports retries and controlled processing.

### Batch vs. Streaming

- **Batch inference:** Process many requests together. It improves efficiency for offline jobs such as document classification or summarization.
- **Streaming inference:** Send generated tokens to the user as they become available. It improves perceived responsiveness for chat applications.

### Microservices and Serverless

- A microservice can separate prompting, retrieval, model serving, and safety checks.
- Serverless functions are useful for API routing, preprocessing, orchestration, and lightweight workloads.
- Large model inference often needs long-lived GPU infrastructure instead of a short-lived function.

## 4. RAG Architecture

**Retrieval-Augmented Generation (RAG)** gives an LLM relevant external information before it generates an answer.

```text
Documents -> Clean -> Chunk -> Embed -> Vector database
                                             |
User question -> Embed -> Search -> Context -> Prompt -> LLM -> Answer
```

### RAG Ingestion Steps

1. Load documents from files, databases, or cloud storage.
2. Clean and normalize the text.
3. Split text into chunks.
4. Create an embedding for each chunk.
5. Store vectors, text, metadata, and document IDs.

### RAG Query Steps

1. Convert the user question into an embedding.
2. Search for similar chunks in the vector database.
3. Filter by metadata such as user, department, or date.
4. Optionally rerank the retrieved results.
5. Add the best context to the prompt.
6. Generate an answer and provide citations when possible.

### Chunking Guidelines

- Very large chunks may contain irrelevant information.
- Very small chunks may lose important context.
- Use a suitable overlap so related sentences are not separated.
- Prefer structure-aware splitting by headings, paragraphs, or sections.
- Store metadata to improve filtering and source tracking.

### Vector Database Operations

- Create and update indexes.
- Insert, replace, or delete document vectors.
- Search by similarity and metadata.
- Re-embed documents when the embedding model changes.
- Track index versions so a result can be reproduced.
- Remove outdated or unauthorized documents quickly.

Examples include managed vector search services, PostgreSQL with pgvector, OpenSearch, Milvus, and other vector databases.

## 5. Prompt and Feature Stores

### Prompt Store

A prompt store manages prompt templates and system instructions as versioned artifacts.

It should support:

- Version history and approvals.
- Environment promotion from development to production.
- A/B testing and rollback.
- Variable and context management.
- Links to evaluation results.

### Feature Store

In traditional ML, a feature store provides standardized features for training and serving. In LLM applications, similar shared data services may manage user context, conversation state, retrieval features, and reusable metadata.

Together, prompt and feature/context stores reduce duplication and make LLM behavior easier to reproduce and control.

## 6. Safety and Governance

LLM applications need protection before, during, and after generation.

- Filter harmful or disallowed input and output.
- Detect prompt injection and attempts to bypass instructions.
- Prevent secrets and personal data from entering prompts or outputs.
- Apply access control to documents used by RAG.
- Log requests safely without storing sensitive content unnecessarily.
- Enforce an output schema for structured responses.
- Use human review for high-impact decisions.
- Test for bias, toxicity, hallucination, and unsafe tool use.

### Advanced Techniques

- **RLHF:** Uses human feedback to improve model behavior.
- **Constitutional AI:** Uses written principles and self-critique to guide safer responses.
- **Guardrails:** Rules, classifiers, scanners, and policy checks around the model.
- **Schema enforcement:** Forces output into a required JSON or structured format, reducing parsing errors.

Safety is a continuous process. It needs evaluation datasets, monitoring, incident handling, and regular updates.

## 7. Performance and Cost Optimization

- **Batching:** Process multiple requests together to use hardware efficiently.
- **Quantization:** Use lower-precision model weights to reduce memory and potentially improve speed.
- **Prompt compression:** Remove unnecessary context and repeated instructions.
- **Caching:** Reuse embeddings, retrieval results, or repeated model responses.
- **Model routing:** Use a smaller model for simple tasks and a stronger model for difficult tasks.
- **Output limits:** Set a reasonable maximum response length.
- **Context control:** Send only relevant retrieved chunks.
- **Autoscaling:** Match compute capacity to demand.
- **Resource forecasting:** Estimate traffic, tokens, GPU memory, latency, and growth before deployment.

Track cost per request, tokens per feature, latency percentiles, error rates, throughput, and GPU utilization.

## 8. CI/CD for LLM Applications

LLM CI/CD includes normal software tests plus tests for model behavior.

### Pipeline Checks

- Unit and integration tests for application code.
- Prompt template and tool integration tests.
- Retrieval tests for relevance and access control.
- Schema and output parsing tests.
- Evaluation sets for quality, factuality, safety, and regression.
- Latency, throughput, and cost tests.
- Security tests for prompt injection and data leakage.

### Safe Releases

- **Canary release:** Send a small percentage of traffic to the new version.
- **A/B testing:** Compare two versions using agreed quality and business metrics.
- **Blue/green release:** Run old and new environments and switch traffic after validation.
- Keep rollback versions for models, prompts, indexes, and application code.

LLM releases are different from traditional software because a code change, prompt change, model change, or retrieval-index change can alter behavior even when the application still runs successfully.

## 9. Lightweight FastAPI RAG Service

A minimal service can expose a question endpoint:

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/ask")
def ask(question: str):
    context = search_vector_database(question)
    answer = call_llm(question, context)
    return {"answer": answer, "sources": context}
```

A production version should add authentication, request validation, timeouts, rate limiting, logging, safe error handling, source citations, and monitoring. The vector search and LLM call should be kept in separate modules so they can be tested independently.

## Quick Recap

- Choose hosted APIs for speed and self-hosting for control, privacy, or predictable high traffic.
- Package weights, tokenizers, prompts, retrieval indexes, dependencies, and settings together.
- Use synchronous APIs for short interactive requests and asynchronous or batch processing for long jobs.
- RAG uses chunking, embeddings, vector search, metadata filtering, and context-aware prompting.
- Prompt stores and model registries provide versioning, approvals, and rollback.
- Safety requires guardrails, schema enforcement, privacy controls, testing, and monitoring.
- Batching, quantization, caching, prompt compression, and model routing reduce cost and latency.
- LLM CI/CD must test both software correctness and generated behavior.
