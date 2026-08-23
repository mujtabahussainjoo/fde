# Agentic AI in Action: Hands-On with LangChain

**Date and time:** 2026-08-22 11:45:39

## 1. What Is LangChain?

**LangChain** is a framework that connects large language models (LLMs) with prompts, processing steps, memory, and tools.

It helps developers build useful applications such as chains, chatbots, and agents without connecting every part manually.

**Simple example:** A prompt asks for three ideas, the LLM generates them, and another prompt summarizes the ideas.

**Memory shortcut:** LangChain helps you **connect, process, remember, and act**.

## 2. Basic LangChain Chain

A **chain** is a sequence of connected steps.

A simple chain usually contains:

1. **Prompt template:** Creates the instruction.
2. **LLM:** Generates a response.
3. **Output parser:** Converts the response into a useful format.

```text
Input -> Prompt Template -> LLM -> Output Parser -> Result
```

### Example: Motivation Quote Generator

The input is a profession such as `teacher` or `coder`.

```python
chain = motivation_prompt | llm | StrOutputParser()
result = chain.invoke({"profession": "teacher"})
```

The prompt is filled with the profession, sent to the model, and returned as plain text.

## 3. Connecting LangChain to Gemini

LangChain can use Google Gemini through the `langchain-google-genai` integration.

Typical setup steps are:

1. Install LangChain and the Gemini integration.
2. Store the Gemini API key securely.
3. Create a Gemini chat model.
4. Send a test prompt.
5. Use the model inside a chain.

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7
)
```

- **Model:** Selects the LLM to use.
- **Temperature:** Controls creativity. A higher value usually gives more varied answers.
- **API key:** Authenticates access to the model and should not be hard-coded in shared code.

## 4. PromptTemplate

A **PromptTemplate** is a reusable prompt with placeholders.

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Give one short motivational quote for a {profession}."
)
```

The `{profession}` value can change for every request.

**Why it helps:** You write the prompt once and reuse it with many inputs.

**Example inputs:**

- `teacher`
- `coder`
- `doctor`

## 5. Sequential Chains

A **sequential chain** sends the output of one step into the next step.

```text
Topic -> Generate Ideas -> Summarize Ideas -> Final Result
```

### Example

1. The first prompt generates three ideas about a topic.
2. The second prompt receives those ideas.
3. The second prompt summarizes them in simple language.

```python
sequential_chain = {
    "ideas": idea_chain,
    "topic": RunnablePassthrough()
} | summary_prompt | llm | StrOutputParser()
```

- **`idea_chain`:** Creates the ideas.
- **`RunnablePassthrough()`:** Sends the original topic forward.
- **`summary_prompt`:** Uses the topic and ideas to create a summary.

**Simple example:**

```text
Topic: Improve school homework feedback
       |
       v
Three creative ideas
       |
       v
Two-sentence beginner-friendly summary
```

**Memory shortcut:** A sequential chain is a **pipeline: one step feeds the next**.

## 6. Chatbot Without Memory

A chatbot without memory treats every request as a new, separate request.

```text
Message 1 -> Response 1
Message 2 -> Response 2
```

It does not automatically remember what was said in Message 1 when it receives Message 2.

**Example:**

1. User: “My name is Asha.”
2. Bot: “Nice to meet you, Asha.”
3. User: “Do you remember my name?”
4. Bot: “I do not remember.”

This happens because each chain runs independently and no conversation history is supplied.

**Use when:** Each request should be independent and past context is not needed.

## 7. ConversationBufferMemory

**ConversationBufferMemory** stores the complete conversation history and sends it to the chatbot during later turns.

```text
Message 1 + Response 1 + Message 2 + Response 2 -> Current context
```

### How It Works

1. The user sends a message.
2. The chain generates a response.
3. Both messages are saved in memory.
4. The saved history is included in the next prompt.

**Example:**

1. User: “My name is Asha.”
2. Bot: “Nice to meet you, Asha.”
3. User: “Do you remember my name?”
4. Bot: “Yes, your name is Asha.”

### Basic Setup

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="input",
    output_key="text",
    return_messages=True
)
```

- **`memory_key`:** Name used for history in the prompt.
- **`input_key`:** Field containing the user's message.
- **`output_key`:** Field containing the chatbot response.
- **`return_messages`:** Returns the history as messages.

The prompt must include the history, for example:

```text
Chat History: {chat_history}
Human: {input}
AI:
```

**Use when:** The chatbot needs full conversation context.

## 8. ConversationBufferWindowMemory

**ConversationBufferWindowMemory** remembers only the most recent part of a conversation.

The `k` value controls how many recent conversation turns are kept.

```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    input_key="input",
    output_key="text",
    k=2,
    return_messages=True
)
```

With `k=2`, the chatbot keeps only the latest two turns or interaction pairs, depending on the library version and configuration.

### Example

1. User gives their name.
2. User asks about Mars.
3. User asks how plants make food.
4. Older information may leave the window.
5. The chatbot may no longer remember the name.

### Why Use Window Memory?

- Keeps prompts smaller.
- Reduces token usage and cost.
- Focuses on recent context.
- Prevents very long conversations from overwhelming the model.

**Trade-off:** It is more efficient, but older details may be forgotten.

**Memory shortcut:** Full buffer remembers **everything**; window buffer remembers **the latest part**.

## 9. Memory Comparison

| Approach | What it remembers | Best use |
| --- | --- | --- |
| **No memory** | Nothing between separate calls | Independent requests |
| **ConversationBufferMemory** | The full conversation | Long, context-rich conversations |
| **ConversationBufferWindowMemory** | Only recent conversation turns | Long chats where recent context matters most |

## 10. Complete Learning Flow

```text
Create model
    -> Create reusable prompt
    -> Build a simple chain
    -> Connect multiple steps
    -> Build a chatbot
    -> Add full memory
    -> Limit memory with a window
```

### Practical Project Example

Build a study assistant that:

1. Receives a topic from a student.
2. Generates three study ideas.
3. Summarizes the ideas.
4. Chats with the student.
5. Remembers the conversation.
6. Keeps only recent turns when the conversation becomes long.

## 11. Important LangChain Ideas

- **LLM:** The language model that generates text.
- **PromptTemplate:** A reusable instruction with variables.
- **Chain:** Connected processing steps.
- **Sequential chain:** A chain where one output becomes the next input.
- **Output parser:** Converts model output into a convenient format.
- **Memory:** Stores conversation context.
- **Full buffer memory:** Keeps the complete history.
- **Window memory:** Keeps only recent history.
- **`invoke()`:** Runs a chain with input data.

## 12. Final Revision Summary

- LangChain connects prompts, models, parsers, memory, and tools.
- A basic chain is usually **prompt -> LLM -> parser**.
- `PromptTemplate` makes prompts reusable.
- Sequential chains pass output from one step to another.
- A chatbot without memory forgets previous requests.
- `ConversationBufferMemory` keeps the full conversation.
- `ConversationBufferWindowMemory` keeps only recent conversation turns.
- Full memory gives more context but uses more tokens.
- Window memory saves resources but may forget older details.

**One-line memory trick:** LangChain builds pipelines, and memory helps chatbots keep the right context.
