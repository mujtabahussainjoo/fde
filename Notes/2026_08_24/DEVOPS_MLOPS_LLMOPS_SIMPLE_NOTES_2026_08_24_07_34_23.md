# DevOps, MLOps, and LLMOps

**Created:** 2026-08-24 07:52:00

## Course Overview

DevOps provides the foundation for reliable software delivery. MLOps extends DevOps to machine learning by managing data, features, training, and models. LLMOps is a specialized form of MLOps for large language model applications.

## 1. DevOps Foundation

DevOps combines development, testing, release, and operations teams across the complete product lifecycle. It grew from Agile ideas such as collaboration, flexibility, short iterations, and continuous improvement.

### Main Practices

- Share ownership and responsibility across teams.
- Use version control and frequent code changes.
- Automate builds, tests, releases, and infrastructure.
- Monitor metrics, logs, traces, and alerts.
- Learn from feedback and improve repeatedly.

### CI/CD

- **Continuous Integration (CI):** Frequently merge code into a shared repository and run code-quality, unit, and integration tests.
- **Continuous Delivery:** Automatically send tested changes to staging; production release needs manual approval.
- **Continuous Deployment:** Automatically release tested changes to production.
- **Infrastructure as Code (IaC):** Use version-controlled YAML or JSON with tools such as Terraform or CloudFormation to create infrastructure. IaC helps prevent configuration drift between environments.

```text
Code -> Build -> Test -> Release -> Deploy -> Monitor -> Improve
```

## 2. What Is MLOps?

**MLOps = Machine Learning + DevOps + Data Engineering**

MLOps makes ML development, deployment, monitoring, and retraining repeatable and automated.

```text
Data -> Validate -> Prepare -> Train -> Evaluate
     -> Register -> Deploy -> Monitor -> Retrain
```

Unlike a normal software pipeline, an ML pipeline must manage code, data, features, preprocessing, model versions, parameters, evaluation results, and serving infrastructure. Data, code, and models are peer dependencies, and each can change independently.

### Continuous Training

MLOps adds **continuous training (CT)** to CI/CD. Retraining may be triggered by:

- A schedule, such as daily or weekly.
- New labeled training data.
- A manual request.
- Reduced model performance.
- Significant data or concept drift.

## 3. DevOps Compared with MLOps

| DevOps | MLOps |
|---|---|
| Code is the main artifact. | Code, data, features, and models all matter. |
| Code is relatively controlled. | Real-world data is messy and unpredictable. |
| Tests focus on code behavior. | Tests also check schemas, data quality, and model performance. |
| Deployment releases a software build. | Deployment releases a model with its preprocessing and serving pipeline. |
| Monitoring checks service health. | Monitoring also checks drift, accuracy, bias, and model decay. |
| Rollback usually restores code. | Rollback may restore code, data, features, and a previous model. |

Using one pipeline for training and prediction helps reduce **training-serving skew**, where preprocessing differs between training and production.

## 4. ML Production Challenges

- **Data quality:** Missing, invalid, incomplete, duplicated, or biased data harms predictions.
- **Schema skew:** Expected features are missing, extra, or have unexpected types or values. The pipeline should usually stop for investigation.
- **Data value skew:** The data schema is valid, but its statistical patterns change. This may trigger retraining.
- **Data drift:** Production inputs differ from training inputs.
- **Concept drift:** The relationship between inputs and outcomes changes.
- **Model decay:** Model performance decreases over time.
- **Model locality:** A model trained for one population or region may not work well elsewhere.
- **Scalability:** Serving must handle traffic, concurrency, latency, and resource limits.
- **Explainability:** Decisions may need to be understandable for trust, debugging, fairness, and compliance.
- **Reproducibility:** Teams must recreate the exact code, data, dependencies, parameters, and model.
- **Versioning:** Data, features, models, configurations, and pipeline components need tracked versions.

## 5. MLOps Maturity Levels

### Level 0: Manual Process

- Data analysis, preparation, training, evaluation, and deployment are manual.
- Work often happens interactively in notebooks.
- Data science and operations may work in silos.
- Releases are infrequent and model monitoring is limited.

### Level 1: Automated ML Pipeline

- Orchestration automates validation, preparation, training, evaluation, and model validation.
- Reusable components support rapid experimentation.
- The same pipeline can be used in development and production.
- Feature stores, model registries, and metadata stores improve reuse and traceability.
- Some deployment and testing may still be manual.

### Level 2: CI/CD/CT Automation

- Code changes automatically build and run tests.
- Pipeline and model artifacts are automatically deployed.
- Continuous training runs from schedules or production triggers.
- Monitoring feeds back into new training and deployment cycles.

## 6. Google Cloud MLOps Architecture

- **Cloud Storage / BigQuery:** Store datasets, features, and prediction data.
- **Vertex AI Workbench:** Explore data and develop models.
- **Vertex AI Pipelines:** Orchestrate ML workflows.
- **Vertex AI Experiments:** Compare training runs.
- **Vertex AI Model Registry:** Manage approved model versions.
- **Vertex AI Endpoints:** Serve online predictions.
- **Vertex AI Model Monitoring:** Detect drift and production problems.
- **Artifact Registry / Cloud Build:** Store artifacts and automate builds.

A **feature store** provides shared feature definitions and supports both batch training and low-latency serving. An **ML metadata store** records parameters, component versions, executors, artifacts, and previous models.

## 7. LLMOps

LLMOps manages the lifecycle of LLM-powered applications. It shares MLOps principles but adds concerns caused by generative, variable, and token-based systems.

### Important LLMOps Practices

- Version prompts, system instructions, tools, datasets, and retrieval indexes.
- Evaluate quality, relevance, tone, factuality, and safety using human review or automated judges.
- Monitor hallucinations, bias, toxicity, prompt injection, and PII leakage.
- Track tokens, context length, latency, errors, and inference cost.
- Use caching, model routing, budgets, and output limits to control cost.
- Use RAG with a vector database to provide current external information.
- Fine-tune an existing foundation model when prompt engineering and RAG are not enough.

MLOps emphasizes feature engineering and statistical metrics such as accuracy or F1. LLMOps emphasizes prompt engineering, subjective output evaluation, safety, and ongoing inference cost.

## 8. LLM Deployment Workflow

1. Select a foundation model.
2. Design and version prompts.
3. Evaluate quality, safety, and business alignment.
4. Improve prompts, add RAG, or fine-tune the model.
5. Deploy using A/B, canary, or blue/green testing.
6. Monitor responses, cost, latency, and safety.
7. Use feedback to improve the next version.

## Quick Recap

- DevOps automates reliable software delivery.
- MLOps adds data, model, feature, and continuous-training management.
- ML operations are harder because real-world data changes independently from code.
- Level 1 focuses on orchestrated pipelines, rapid iteration, and validation.
- Level 2 adds automated CI/CD/CT and closed-loop monitoring.
- LLMOps specializes in prompts, RAG, safety, subjective evaluation, and token cost.
