# Large Language Models and Key Metrics

**Created:** 2026-08-25 09:07:03
**Topic:** LLM architecture, concepts, model selection, and evaluation metrics

## 1. Course Overview

A **Large Language Model (LLM)** is an artificial intelligence model trained on very large collections of text. It learns patterns in language so it can understand prompts and generate useful text. LLMs are used for question answering, chatbots, translation, summarization, content generation, sentiment analysis, and information extraction.

The quality of an LLM should not be judged by one score alone. A good evaluation combines language quality, task performance, speed, cost, safety, and user or business outcomes.

## 2. LLM Architecture

Most modern LLMs are based on the **Transformer architecture**. Its main parts are:

- **Tokenization:** Splits text into tokens such as words, subwords, or characters.
- **Input embeddings:** Converts token IDs into numerical vectors that represent learned meaning.
- **Positional encoding:** Adds information about the order of tokens, because attention by itself does not know sequence position.
- **Self-attention:** Calculates how strongly each token should relate to other tokens in the same input. This helps the model use context.
- **Multi-head attention:** Runs several attention patterns at the same time so different heads can learn different relationships.
- **Feed-forward layers:** Further transform the information collected by attention.
- **Transformer blocks:** Repeated attention and feed-forward layers that gradually build a richer representation.
- **Decoder or output layer:** Predicts the next token or produces an output for a specific task.

A simplified flow is:

```text
Text -> Tokens -> Embeddings + Positions -> Transformer blocks -> Output tokens
```

Attention improves contextual understanding, but larger attention workloads can increase latency, memory use, and computational cost. Model design is therefore a trade-off between quality, speed, and expense.

## 3. Important LLM Concepts

### Natural Language Understanding and Generation

- **Natural Language Understanding (NLU):** The ability to interpret text, identify intent, extract information, and analyze meaning or sentiment.
- **Natural Language Generation (NLG):** The ability to produce coherent and contextually appropriate text.

### Self-Supervised Learning

**Self-supervised learning** trains a model using labels created from the data itself. For example, the model can hide or predict the next token in a sentence. This makes it possible to learn from huge amounts of mostly unlabeled text.

### Pre-training and Fine-tuning

- **Pre-training:** The model learns general language patterns from a broad dataset.
- **Fine-tuning:** The pre-trained model is adapted to a particular task, industry, style, or domain using more specific data.

This is an example of **transfer learning**, where knowledge learned from one broad task is reused for another task. It reduces the time and resources needed compared with training a new model from the beginning.

### Embeddings

An **embedding** is a dense numerical representation of text. Similar meanings tend to have similar vector representations. Context can change an embedding, so the word "bank" can be represented differently when referring to money or a river.

## 4. Core Principles and Limitations

LLMs are data-driven, context-aware, adaptable, and capable of learning useful language representations. Their versatility allows them to support many domains, especially after fine-tuning.

Important limitations include:

- Training and inference can require expensive GPUs, memory, storage, and energy.
- Increasing model size eventually gives smaller performance improvements for the added cost.
- Results depend strongly on the quality, coverage, and freshness of the training data.
- Bias in the data can produce unfair or harmful outputs.
- Low-resource languages and specialized fields may have insufficient training data.
- Real-time use can be difficult when model size causes high latency.
- A fluent answer is not necessarily a truthful or reliable answer.

Useful improvements include better data curation, bias testing, fairness methods, model pruning, quantization, distillation, smaller specialized models, and continuous evaluation.

## 5. Types of LLMs

### Public LLMs

A **public LLM** is provided by an external company, commonly through a hosted application or API. It is usually pre-trained, easy to integrate, and scalable.

**Advantages:**

- Fast deployment with little infrastructure.
- Predictable access and provider-managed updates.
- Good general-purpose performance.
- Easy scaling for changing demand.

**Disadvantages:**

- Limited control and customization.
- Sensitive data may need to be sent to a third-party service.
- Usage or subscription costs can grow with volume.
- Availability depends on the provider's infrastructure and policies.

### In-house LLMs

An **in-house LLM** is developed, hosted, or maintained by an organization for its own requirements. It can use proprietary data and specialized workflows.

**Advantages:**

- Strong control over data, architecture, updates, and deployment.
- High customization for specialized terminology and tasks.
- Better ability to meet strict privacy or compliance requirements.
- Tailored performance for a specific domain.

**Disadvantages:**

- High development and infrastructure costs.
- Requires GPUs, storage, maintenance, and specialist staff.
- Training or fine-tuning can take a long time.
- The organization is responsible for security, monitoring, updates, and reliability.

### Open-source LLMs

An **open-source LLM** provides model code or weights under an applicable license and can often be deployed on an organization's own infrastructure. It offers more control than a typical public service, but effective deployment still requires technical expertise and computing resources.

## 6. Selecting an LLM

Selection should begin with the business problem, not the model name. Define the task, users, data sensitivity, expected quality, and operational constraints.

Key criteria are:

- **Task-specific performance:** How well the model performs the intended task, such as translation, classification, summarization, or question answering.
- **Computational requirements:** Required GPU or CPU capacity, memory, storage, and energy.
- **Scalability:** Ability to handle increasing users, requests, data volume, or workload.
- **Latency:** Time required to return a response.
- **Throughput:** Amount of work or number of requests processed in a period.
- **Cost:** Upfront infrastructure and licensing costs plus ongoing inference, maintenance, and update costs.
- **Privacy and compliance:** Whether data handling satisfies legal, security, and industry requirements.
- **Customization:** Ability to use fine-tuning, retrieval, prompting, or workflow integration.
- **Reliability and support:** Availability, monitoring, service support, and provider or community stability.

Horizontal scaling adds more machines, while vertical scaling increases the power of an existing machine. Cloud-native deployment can scale flexibly, but pay-as-you-go costs must be monitored. The best choice balances performance, scalability, security, and total cost of ownership.

## 7. Common Evaluation Metrics

### Perplexity

**Perplexity** measures how uncertain a language model is when predicting the next token in a sequence. It is commonly calculated from the model's average loss:

$$
\text{Perplexity} = e^{\text{average loss}}
$$

Lower perplexity generally means the model predicts the evaluation text more confidently. It is most useful when comparing models on the same dataset and evaluation setup. A score is not meaningful by itself because text difficulty and domain affect it.

### BLEU

**BLEU (Bilingual Evaluation Understudy)** compares generated text with one or more reference texts using matching n-grams. It is widely used for machine translation.

A higher BLEU score indicates more overlap with the reference. However, BLEU may penalize valid wording that differs from the reference and can be affected by short outputs or poor reference text.

### ROUGE

**ROUGE (Recall-Oriented Understudy for Gisting Evaluation)** compares a generated summary with a reference summary. Common variants include:

- **ROUGE-N:** Overlap of n-grams.
- **ROUGE-L:** Overlap based on the longest common subsequence.

ROUGE is useful for checking whether important reference content appears in a summary, but it cannot fully judge clarity, factuality, or meaning.

### Precision, Recall, and F1

- **Precision:** Of the items predicted as relevant, the proportion that was actually relevant.
- **Recall:** Of all relevant items, the proportion the model found.
- **F1 score:** The harmonic mean of precision and recall.

$$
F1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
$$

F1 ranges from 0 to 1. It is useful for classification and extraction when both missed items and incorrect items matter.

### Accuracy

**Accuracy** is the proportion of predictions that are correct:

$$
\text{Accuracy} = \frac{\text{Correct predictions}}{\text{Total predictions}}
$$

Accuracy can be misleading for imbalanced classes, so it should sometimes be combined with precision, recall, and F1.

### Loss Function

A **loss function** measures the difference between the model's prediction and the expected target during training or evaluation. Training attempts to minimize loss. For language modeling, token-level cross-entropy loss is commonly related to perplexity.

### Human Evaluation

**Human evaluation** uses reviewers to assess qualities that automated metrics often miss, including correctness, coherence, fluency, relevance, helpfulness, tone, safety, and factuality. Reviewers need clear criteria and consistent scoring to reduce subjectivity.

### Benchmarks

**GLUE** and **SuperGLUE** are benchmark suites containing multiple language understanding tasks, such as inference, sentiment analysis, and question answering. They enable standardized comparisons, but benchmark performance may not predict performance in a particular business workflow.

**HELM** is a broad evaluation framework intended to assess language models across multiple scenarios and dimensions, such as accuracy, robustness, fairness, bias, toxicity, and efficiency.

**EleutherAI evaluation tests** are collections of standardized language-model tasks and benchmarks used to compare model capabilities across different areas.

### Latency and Efficiency

**Latency** is the time taken to produce a response. **Efficiency** describes how much compute, memory, energy, or cost is needed for a given amount of useful work. Real-time systems usually need low latency and sufficient throughput, so model compression and optimized serving can be important.

## 8. Intrinsic and Extrinsic Evaluation

### Intrinsic Evaluation

**Intrinsic evaluation** measures the model's internal language behavior independently of a complete application. Examples include perplexity, token loss, BLEU, ROUGE, and language-quality checks.

It is useful during development for diagnosing prediction quality, grammar, syntax, and contextual behavior. It does not prove that the model will deliver business value.

### Extrinsic Evaluation

**Extrinsic evaluation** measures how well the model performs in a real task or application. Examples include customer-query resolution, sentiment classification accuracy, task completion rate, user satisfaction, escalation rate, factuality, and response time.

It requires realistic test data and a defined testing framework. Extrinsic results are closer to production value, but they can change when users, workflows, or requirements change.

Both approaches are needed. A model can have strong language metrics but fail to solve customer problems, or have acceptable task performance while still having internal weaknesses that need monitoring.

## 9. Aligning Metrics with Business Use Cases

Metrics must reflect the purpose of the system:

| Use case | Important metrics |
| --- | --- |
| Customer service chatbot | Accuracy, task completion, latency, user satisfaction, escalation rate, safety |
| Machine translation | BLEU, human quality review, terminology accuracy, latency |
| Summarization | ROUGE, factuality, coverage of important information, human review |
| Sentiment or intent classification | Accuracy, precision, recall, F1, class-level performance |
| Content generation | Relevance, coherence, factuality, human preference, cost, latency |
| Real-time voice or chat | Latency, throughput, availability, task success, user satisfaction |
| Regulated healthcare or finance | Accuracy, factuality, privacy, fairness, auditability, compliance, safety |

Metric selection should account for trade-offs. Higher accuracy may increase latency and cost. Lower cost may reduce quality. A creative writing system may prioritize coherence and human preference, while a support system may prioritize correctness, safety, and resolution rate.

Best practices are to define a baseline, involve technical and business stakeholders, evaluate on representative data, combine automated and human checks, monitor continuously, and revise metrics as the application changes.

## 10. Practical LLM Demonstrations

### Basic Architecture Demonstration

A simple Transformer demonstration can use Hugging Face tokenizers and models:

1. Tokenize a sentence and return token IDs.
2. Pass the IDs through a pre-trained model to obtain hidden-state embeddings.
3. Inspect attention weights to see relationships between tokens.
4. Use a text-generation pipeline to continue a prompt.
5. Use summarization and question-answering pipelines for task examples.

A pre-trained BERT model can produce embeddings and attention visualizations, while a GPT-style model is suitable for text generation. Outputs are probabilistic and should be reviewed rather than treated as guaranteed facts.

### Evaluation Demonstration

A practical evaluation can use a pre-trained GPT-2 model and a test dataset:

- **Perplexity:** Tokenize evaluation text, calculate model loss, average the loss, and exponentiate it. Lower values are better only when comparing equivalent evaluation conditions.
- **BLEU:** Generate text and compare it with reference text using n-gram overlap. The score ranges from 0 to 1, but acceptable values depend on the task and dataset.
- **F1:** Compare predicted labels with ground-truth labels to measure the balance between precision and recall.
- **Task accuracy:** Run a sentiment-analysis model over labeled reviews and divide correct predictions by the number of examples.

The reported sample results illustrate the method, not universal quality thresholds. Evaluation datasets, preprocessing, model choice, and task difficulty all affect the numbers.

## 11. Final Summary

LLMs use Transformer-based components such as tokenization, embeddings, positional information, attention, and feed-forward layers to process and generate language. Pre-training provides general capability, while fine-tuning and other adaptation methods specialize a model.

Public models are convenient and scalable, in-house models provide maximum control and privacy, and open-source models offer flexibility with deployment responsibility. Model selection should balance task performance, resources, scalability, cost, latency, security, and compliance.

Perplexity, BLEU, ROUGE, F1, accuracy, loss, human review, HELM, EleutherAI tests, GLUE, SuperGLUE, latency, and efficiency each measure different aspects of quality. Intrinsic metrics examine model behavior; extrinsic metrics examine practical results. A reliable evaluation strategy combines both and aligns them with the actual business goal.
