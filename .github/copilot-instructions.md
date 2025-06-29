# Python Agent Development Kit (ADK) Copilot Instructions

## Key Principles
- Write concise, technical code with accurate Python examples, focusing on **agent capabilities and interactions**.
- Prefer **functional design for tools and agents**; avoid unnecessary classes.
- Favor **modularity** for agents, tools, and callbacks over code duplication.
- Use **descriptive variable names** (e.g., `is_active`, `has_permission`, `weather_tool`).
- Use `lowercase_with_underscores` for directories and files, consistent with Python best practices.
- Favor **named exports/definitions** for agents, tools, and utility functions.
- Use the **Receive an Object, Return an Object (RORO) pattern** for tool inputs and outputs where appropriate, often with Pydantic models.

---

## ADK Framework Guidelines
- Use `def` for **synchronous tool functions and callbacks**, and `async def` for **asynchronous tools** (e.g., those interacting with external APIs or databases).
- Use **type hints** for all function signatures, especially for tool inputs and outputs.
- Prefer **Pydantic models for defining structured inputs and outputs for tools** and for representing complex session state.
- File structure: organize by **agents, sub-agents, tools, callbacks, and data models (schemas)**.
- Use concise, one-line syntax for simple conditionals within agent instructions or tool logic.

---

## Agent and Tool Design
- **Agent Descriptions & Instructions:** Provide clear, concise `description` for agent delegation and detailed `instruction` prompts for the LLM to understand its role, persona, and how to use its tools effectively.
- **Tool Definition & Docstrings:** Define tools as Python functions. **Crucially, use descriptive docstrings** that explain the tool's purpose, arguments, and return values. The LLM relies on these docstrings to decide when and how to use a tool.
- **Multi-model Flexibility:** Leverage **`LiteLlm`** to easily integrate and switch between various LLMs (e.g., Gemini, GPT, Claude) for different agents or tasks.
- **Agent Delegation:** Design agents with clear responsibilities and utilize ADK's delegation features (e.g., `auto_flow`) for intelligent routing between specialized sub-agents.
- **Session State:** Use **`Session State` and `ToolContext`** to give agents memory and enable contextual interactions across conversational turns.

---

## Error Handling and Validation
- Handle errors and edge cases **at the start of tool functions** or within agent instructions.
- Use **early returns for error conditions** in tools; avoid deep nesting.
- Place the **happy path last** in tool functions.
- Avoid unnecessary `else` statements; use the `if-return` pattern.
- Use **guard clauses** for preconditions and invalid states in tool implementations.
- Implement proper **error logging** and design agents to provide **user-friendly error messages**.
- Use **custom error types or factories** for consistent error handling within tools.
- Utilize **ADK's callback system** (`before_model_callback`, `before_tool_callback`, `on_error_callback`) for inspecting, modifying, or blocking requests/tool usage and for global error monitoring.

---

## Dependencies
- `google-adk` (core framework)
- `litellm` (for multi-model support)
- Asynchronous database libraries (e.g., `asyncpg`, `aiomysql`) for tools interacting with databases.
- `SQLAlchemy 2.0` (if using ORM within tools).
- `Pydantic v2` (for data validation and modeling).

---

## Performance Optimization
- **Minimize blocking I/O** in agents and tools; use `async` for database and external API calls within tools.
- Implement **caching** for static or frequently accessed data when retrieved by tools (e.g., using Redis for tool results).
- Optimize **serialization/deserialization** with Pydantic for efficient tool input/output.
- Consider **lazy loading** for large datasets processed by tools.

---

## Key Conventions
- Prioritize **API performance metrics** for your agentic application (response time, latency, throughput).
- Limit blocking operations in agents; favor **async/non-blocking flows** for agent execution and tool usage.
- Use **dedicated async functions for tools** that perform database and external API operations.
- Structure **agents, tools, and dependencies** for readability and maintainability, promoting a clear separation of concerns.
- Utilize **ADK's `Runner` and `SessionService`** to orchestrate agent execution and manage conversational state effectively.

Refer to the [ADK documentation](https://google.github.io/adk-docs/get-started/) for best practices on Agent definition, Tool usage, Session management, and Callbacks.