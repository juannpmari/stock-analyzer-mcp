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
        "stockanalyzermcp:latest"
      ]
    }
```