# Agentic AI in Action: Controlled Workflows with LangGraph

**Date and time:** 2026-08-22 11:53:15

## 1. What Is LangGraph?

**LangGraph** is a framework for building controlled, structured AI workflows.

It helps developers define exactly how data and decisions move through an AI system. This makes multi-step workflows easier to understand, test, debug, and improve.

**Simple example:** A chatbot receives a message, analyzes it, creates a response, formats the response, and then finishes through clearly connected workflow steps.

**Memory shortcut:** LangGraph is a **map for AI steps and decisions**.

## 2. The Four Core Components

Remember: **StateGraph, Nodes, Edges, State**.

| Component | Simple definition | Example |
| --- | --- | --- |
| **StateGraph** | The container that holds the complete workflow | The whole chatbot process |
| **Node** | A step or function that performs work | Analyze a user message |
| **Edge** | A connection that controls what runs next | Analyze -> Process |
| **State** | Shared data passed between nodes | User input, messages, status, and result |

### How They Work Together

1. The `StateGraph` defines the workflow structure.
2. Nodes read the current state and perform tasks.
3. Edges decide the next node.
4. State carries information from one step to the next.

**Easy analogy:** The graph is a building, nodes are workers, edges are roads, and state is the shared notebook.

## 3. State Flow

**State** is the shared memory of a workflow. Every node can read relevant fields and return updates.

A state schema is commonly defined with Python's `TypedDict`.

```python
from typing import TypedDict

class ResearchState(TypedDict):
    query: str
    web_results: str
    document_results: str
    final_answer: str
    step_count: int
```

### Example of State Moving Through Nodes

1. **Start:** The state contains a query and an empty result.
2. **Web search node:** Adds web results and increases the step count.
3. **Document search node:** Keeps the web results and adds document results.
4. **Synthesis node:** Reads all previous data and creates the final answer.

State grows as the workflow continues. Later nodes can build on earlier work instead of starting again.

## 4. State Update Patterns

### Replace

The new value overwrites the old value.

```python
{"step_count": 5}
```

**Use for:** Status, progress, current step, or final answer.

### Accumulate

New information is added to existing information.

```python
{"findings": ["New finding"]}
```

**Use for:** Messages, findings, search results, or outputs from repeated steps.

### Merge

New dictionary values are combined with existing dictionary values.

```python
{"metadata": {"source": "web"}}
```

**Use for:** Metadata or grouped information where existing keys should remain.

**Memory shortcut:** Replace **changes**, accumulate **grows**, merge **combines**.

## 5. Linear Workflows

A **linear workflow** follows one fixed sequence every time.

```text
START -> Input -> Analyze -> Process -> Output -> END
```

**Example:** A customer report system always fetches data, calculates metrics, creates charts, and generates a PDF.

### Use Linear Workflows When

- The steps never change.
- No decision or branching is required.
- Predictability and easy debugging are important.

**Analogy:** A linear workflow is like following a recipe.

## 6. Conditional Workflows

A **conditional workflow** chooses a path based on the current state or input.

```text
START -> Classify
             |-> Web Search
             |-> Document Search
             |-> Both
```

**Example:**

- A current-news question goes to web search.
- A company-policy question goes to document search.
- A broad research question goes to both.

### Use Conditional Workflows When

- Different inputs need different treatment.
- The system must adapt to context.
- Some steps should be skipped when they are unnecessary.

**Easy rule:** Fixed numbered steps mean linear. “If this, then that” means conditional.

## 7. Conditional Routing

A **router** is a function that examines state and returns the name of the next node.

```python
def decide_path(state: ResearchState) -> str:
    query = state["query"].lower()

    if "latest" in query or "current" in query:
        return "web_search"
    if "document" in query or "company" in query:
        return "document_search"
    return "both"
```

LangGraph uses the returned node name to select the next path.

## 8. LLM-Based Routing

Instead of simple keyword rules, an LLM can classify the user's intent.

Possible categories include:

- `GREETING`
- `QUESTION`
- `COMMAND`
- `FEEDBACK`
- `UNCLEAR`

The LLM can return:

- **Category:** What type of input is this?
- **Confidence:** How certain is the classification?
- **Reasoning:** Why was this category selected?

### Confidence-Based Routing

1. The LLM classifies the input.
2. The router checks the confidence score.
3. High-confidence input goes to a specialized handler.
4. Low-confidence input goes to a fallback handler.
5. The fallback handler asks the user to clarify.

**Why it helps:** Confidence thresholds prevent the system from confidently taking the wrong path.

## 9. Building a StateGraph

A basic LangGraph build process is:

1. Define the state schema with `TypedDict`.
2. Write node functions.
3. Create a `StateGraph` using the state schema.
4. Add the nodes.
5. Set the entry point.
6. Connect nodes with edges.
7. Add conditional edges when routing is needed.
8. Compile the graph.
9. Invoke it with an initial state.

### Basic Linear Example

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node("input", input_node)
workflow.add_node("analyze", analyze_node)
workflow.add_node("process", process_node)
workflow.add_node("output", output_node)

workflow.set_entry_point("input")
workflow.add_edge("input", "analyze")
workflow.add_edge("analyze", "process")
workflow.add_edge("process", "output")
workflow.add_edge("output", END)

app = workflow.compile()
```

### What Does Compile Mean?

**Compile** converts the graph definition into an executable application.

It validates the structure and creates a runnable object that can receive state and return final state.

**Memory shortcut:** Build the blueprint, then compile the working machine.

## 10. Example: Four-Stage Chatbot

A simple chatbot can contain four nodes:

1. **Input node:** Receives the user's message and adds it to state.
2. **Analyze node:** Identifies whether it is a greeting, weather request, or general question.
3. **Process node:** Creates the suitable response.
4. **Output node:** Formats the result and marks the workflow complete.

```text
User message -> Input -> Analyze -> Process -> Output -> END
```

The state may contain:

- Conversation messages
- Original user input
- Current processing step
- Final result

Nodes return only the fields they want to update. LangGraph merges those updates into the existing state.

## 11. Testing and Visualization

A workflow should be tested with different inputs, such as:

- A greeting
- A technical question
- A command
- Feedback
- An unclear message
- A mixed-intent message

Check the final state for:

- Query type
- Confidence score
- Route taken
- Reasoning
- Final response

A graph visualization can show the workflow structure and make branches, loops, and disconnected nodes easier to find.

## 12. Best Practices

- Start with a linear workflow.
- Add branches only when they solve a real problem.
- Give nodes clear names.
- Keep routing logic simple and readable.
- Define every state field clearly.
- Test every possible route.
- Handle empty or unclear input.
- Add fallback behavior when an LLM or API fails.
- Validate state at important steps.
- Keep API keys in secure storage.
- Log decisions, routes, errors, and results.
- Tell users clearly when the system needs clarification.

## 13. Final Revision Summary

- LangGraph creates structured and transparent AI workflows.
- `StateGraph` holds the workflow.
- Nodes perform tasks.
- Edges control the path.
- State carries shared data and memory.
- Replace overwrites a value.
- Accumulate adds information.
- Merge combines dictionary data.
- Linear workflows use one fixed path.
- Conditional workflows choose paths based on state.
- Routers return the next node name.
- LLM routing can use categories and confidence scores.
- Compilation turns a graph definition into a runnable application.
- Testing every path makes workflows more reliable.

**One-line memory trick:** LangGraph lets AI **carry state through nodes, follow edges, choose paths, and finish as a controlled application**.
