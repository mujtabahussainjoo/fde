# Agentic AI in Action: Tool Use with LangChain

**Date and time:** 2026-08-22 11:46:57

## 1. What Is Tool Use?

**Tool use** allows an AI agent to call external functions, APIs, databases, search engines, or other services.

An LLM is good at language, but tools give it reliable abilities such as exact calculation, live search, weather lookup, and database access.

**Simple example:** Instead of guessing a calculation, the agent calls a calculator tool and returns the exact result.

**Memory shortcut:** The LLM is the **brain**; tools are the **hands**.

## 2. How a LangChain Tool Works

A LangChain tool is usually a safe Python function with a clear name, input, output, and description.

```text
User request -> Agent understands task -> Selects tool -> Sends input -> Tool runs -> Agent uses result
```

### Normal Tool Workflow

1. Receive the user's request.
2. Decide whether a tool is needed.
3. Select the most suitable tool.
4. Prepare the required input or JSON payload.
5. Call the tool.
6. Read and check the result.
7. Use the result in the final answer.
8. Log important outputs or errors.

The `@tool` decorator can turn a normal Python function into a LangChain tool.

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Return a weather report for a city."""
    return f"Weather information for {city}"
```

## 3. Why Tools Are Important

Without tools, an LLM must rely mainly on what it learned during training. This can cause problems with:

- Exact mathematics
- Current news and facts
- Private or business data
- Weather and live conditions
- Database operations
- Actions in external systems

Tools make agent responses more accurate, current, useful, and verifiable.

## 4. Building a Safe Calculator Tool

A calculator tool is a good example of giving an LLM a reliable skill.

### Why Not Let the LLM Do the Math?

LLMs predict text patterns. They are not dedicated arithmetic engines, so they may make mistakes with long or complex calculations.

A calculator function produces deterministic and repeatable results.

### Safe Calculator Principles

- Allow only approved arithmetic operators.
- Parse expressions with Python's `ast` module.
- Reject unsupported syntax.
- Limit the expression length.
- Handle errors clearly.
- Prevent arbitrary code execution.
- Check for extremely large results.

```python
import ast
import operator as op

ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
}
```

The important idea is **allowlisting**: permit only operations that are known to be safe.

### Tool-Based Math vs. Plain LLM Math

| Plain LLM | Calculator tool |
| --- | --- |
| May guess or miscalculate | Produces exact results |
| Uses language prediction | Uses deterministic code |
| No execution safety boundary | Can allow only approved operations |
| Best for explaining math | Best for performing math |

**Memory shortcut:** Ask the LLM to explain the math, but ask the calculator to perform it.

## 5. Connecting a Tool to an Agent

A tool-enabled LangChain agent normally includes:

1. **LLM:** Understands the user's request.
2. **Tool list:** Defines available functions.
3. **Prompt:** Explains when and how to use each tool.
4. **Agent:** Decides the next action.
5. **AgentExecutor:** Runs the agent and tool calls step by step.

```python
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)
result = executor.invoke({"input": "Compute 15 * 23 + 45"})
```

A good prompt can require the agent to always use the calculator for arithmetic instead of calculating in its head.

## 6. Built-In Search Tools

LangChain can connect agents to external knowledge sources through built-in or community tools.

### DuckDuckGo Search

**Definition:** A web-search tool that helps retrieve current information, news, links, and snippets.

**Best for:**

- Latest headlines
- Current events
- Recent facts
- Fresh web information

### Wikipedia

**Definition:** A reference tool that returns background information and summaries from Wikipedia.

**Best for:**

- Definitions
- Historical background
- Biographies
- General reference information

### Choosing the Right Source

- Use **DuckDuckGo** for current or time-sensitive information.
- Use **Wikipedia** for background knowledge and definitions.
- Use both when a question needs current facts and background context.

**Example:** For “What is the latest news about generative AI?” use web search. For “Who was Albert Einstein?” use Wikipedia.

### Good Search-Agent Behavior

- Use tools for facts, dates, and numbers.
- Return source titles and URLs.
- Format raw search results clearly.
- Handle no-result and error cases.
- Avoid inventing information.

## 7. Creating a Custom Weather Tool

A **custom tool** is a function created for a specific business or application need.

A weather tool might accept a city and return:

- City
- Current time
- Condition
- Temperature
- Humidity
- Chance of rain

```python
@tool
def get_weather(city: str) -> str:
    """Return a short weather report for a city."""
    if not city or not city.strip():
        return "Please provide a city name."
    return "Partly cloudy, around 30 C, moderate humidity."
```

The course example uses mock data. Mock data is useful for learning because it is predictable and does not require a live weather API.

Later, the mock function can be replaced with a real API without changing the agent's basic wiring.

### Good Custom Tool Design

- Give the tool one clear responsibility.
- Validate inputs.
- Return structured, readable output.
- Handle missing or unknown values.
- Return useful error messages.
- Keep secrets such as API keys out of source code.
- Add a clear description so the agent knows when to use it.

## 8. Combining Multiple Tools

A multi-tool agent has access to several tools and chooses between them based on the user's task.

Example tools:

- **Calculator:** Exact arithmetic
- **DuckDuckGo:** Current web information
- **Wikipedia:** Background knowledge
- **Weather tool:** Weather data

```text
User question
     -> Agent identifies needed actions
     -> Calculator / Search / Wikipedia / Weather
     -> Agent combines results
     -> Final answer
```

### Example 1: Math

**Question:** `What is 15 * 23 + 45?`

The agent selects the calculator and returns `390`.

### Example 2: Current Fact and Math

**Question:** “Who is the current president of France, and what is the square root of 144?”

1. Use web search for the current fact.
2. Use the calculator for the square root.
3. Combine both results in one answer.

### Example 3: Background and Calculation

**Question:** “Explain Einstein's work and calculate the speed of light in kilometers per second.”

1. Use Wikipedia for background.
2. Use the calculator for the conversion.
3. Present the explanation and exact result together.

**Memory shortcut:** A multi-tool agent **chooses, calls, combines, and explains**.

## 9. Tool Descriptions Guide Decisions

Tool descriptions help the agent understand what each tool does and when to use it.

```python
Tool(
    name="Calculator",
    func=calculator,
    description="Useful for mathematical calculations."
)
```

A clear description should explain:

- The tool's purpose
- The input format
- The type of result returned
- When the tool should be selected

Poor descriptions can cause tool confusion. For example, the agent might use a general LLM response when it should use a calculator or live search.

## 10. Tool Chaining

**Tool chaining** means using the output of one tool as input for another step or tool.

```text
Search database -> Summarize result -> Calculate total -> Email report
```

Tool chaining helps agents solve multi-part tasks that require several different abilities.

The agent should check each result before continuing so one bad output does not spread through the workflow.

## 11. Safety and Reliability

- Allow only approved tools.
- Validate all user inputs and tool parameters.
- Never execute arbitrary code from user text.
- Use allowlists for dangerous operations.
- Keep API keys in secure environment variables.
- Handle timeouts and API failures.
- Return clear error messages.
- Check tool results before using them.
- Log actions and failures.
- Ask for confirmation before important or irreversible actions.
- Use citations for external facts.

**Key principle:** A tool should make an agent more capable without making it uncontrolled.

## 12. Complete Tool-Use Pattern

```text
Understand request
      -> Break into actions
      -> Select the right tool
      -> Prepare safe input
      -> Invoke tool
      -> Check result
      -> Store useful result
      -> Continue or answer
```

### Short Example

A user asks: “Find today's weather in Mumbai, calculate the temperature in Fahrenheit, and summarize it.”

1. Weather tool gets the temperature in Celsius.
2. Calculator converts Celsius to Fahrenheit.
3. LLM summarizes both results.
4. Agent returns a clear answer.

## 13. Final Revision Summary

- Tools let agents use functions, APIs, databases, and live data.
- A Python function can become a LangChain tool with `@tool`.
- Calculators are better than LLMs for exact arithmetic.
- Safe tools use validation and allowlists.
- DuckDuckGo is useful for current web information.
- Wikipedia is useful for background knowledge.
- Custom tools add business-specific abilities such as weather lookup.
- Multi-tool agents choose and chain tools to solve complex questions.
- Tool descriptions help agents select the correct tool.
- Reliable agents validate inputs, check outputs, handle errors, and protect credentials.

**One-line memory trick:** LangChain agents **understand the task, choose the tool, use it safely, check the result, and combine the answer**.
