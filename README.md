# LangGraph LLM Tool Call Demo

This repository demonstrates the integration of LangGraph with OpenAI's GPT models and Google Serper for web search capabilities. It features a chat interface built with Gradio that allows users to interact with an AI assistant that can search the web for current information.

## Features

- 🤖 OpenAI integration
- 🔍 Google Serper web search capabilities
- 💬 Interactive chat interface using Gradio
- 📊 LangGraph for managing conversation flow
- 💾 SQLite-based conversation persistence
- 🛠️ Tool-based architecture for extensibility

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- OpenAI API key
- Google Serper API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/langgraph-llm-tool-call.git
cd langgraph-llm-tool-call
```

2. Create a `.env` file in the project root with your API keys:

```bash
OPENAI_API_KEY=your-openai-api-key
SERPER_API_KEY=your-serper-api-key
```

3. Install dependencies using uv:

```bash
uv sync
```

## Usage

1. Start the chat interface:

```bash
uv run app.py
```

2. Open your browser and navigate to `http://localhost:7860`

3. Start chatting with the AI assistant! You can ask questions that require current information, and the assistant will use web search to provide up-to-date answers.

## Project Structure

- `app.py` - Gradio chat interface implementation
- `graph.py` - LangGraph implementation with tool integration
- `pyproject.toml` - Project dependencies and metadata
- `memory.db` - SQLite database for conversation persistence

## Architecture

The project uses LangGraph to manage the conversation flow between different components:

1. The chat interface (`app.py`) handles user input and displays responses
2. The graph implementation (`graph.py`) manages:
   - LLM integration with OpenAI
   - Web search capabilities via Google Serper
   - Conversation state management
   - Tool execution flow

### Graph Visualization

The following diagram shows the flow of the LangGraph implementation:

![LangGraph Flow](graph.png)

The graph shows how messages flow between the agent and tools nodes, with the agent being able to decide when to use tools based on the conversation context.

## Development

### Adding New Tools

To add new tools to the assistant:

1. Define the tool function in `graph.py`
2. Add it to the `tools` list
3. The LLM will automatically learn to use the new tool

### Modifying the Graph

The graph structure can be visualized by running the application - it will generate a `graph.png` file showing the current flow.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Phillipp Bertram
