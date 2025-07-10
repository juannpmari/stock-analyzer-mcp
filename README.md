# Stock Analyzer MCP

The Stock Analyzer MCP Server is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server that provides seamless integration with [Yahoo Finance API](https://pypi.org/project/yfinance/), enabling advanced automation and interaction capabilities for developers and tools.

## Use cases

- Automate retrieval of stock market data, including current prices, historical prices, and news.
- Providing context for stock market price predictions.
- Building AI powered tools for stock market analysis.


## Usage

### Windsurf
Add the following configuration to mcp_config.json:
```json
"financial-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "ghcr.io/juannpmari/stockanalyzermcp"
      ]
    }
```

### Custom agent
The repository includes a simple custom agent implemented using [Tiny Agents](https://tinyagents.dev/). It uses a Qwen model to answer questions about stock market data.
To run it in the CLI, use the following commands in a bash terminal:
```bash
cd client
pip install "huggingface_hub[mcp]>=0.32.0"
tiny-agents run agent.json
```
