# Stock Analyzer MCP

The Stock Analyzer MCP Server is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) server that provides seamless integration with [Yahoo Finance API](https://pypi.org/project/yfinance/) and [TickerTick API](https://github.com/hczhu/TickerTick-API), enabling advanced automation and interaction capabilities for developers and tools.

![Demo](assets/example.gif)


## Use cases

- Automate retrieval of stock specific data, including current prices and historical prices.
- Automate retrieval of market fundamentals, including earnings dates and earnings reports for each company.
- Provide context for stock market price predictions.
- Build AI-powered tools for stock market analysis.


## Local MCP Server

### Prerequisites

The server is designed to be run locally in a container. You will need to have Docker installed and running.

### Windsurf

Add the following configuration to `mcp_config.json`:
```json
{
    "mcpServers": {
      "financial-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "ghcr.io/juannpmari/stockanalyzermcp"
      ]
    }
  }
}
```

### Cursor

Navigate to Settings > Cursor Settings > MCP and click "Add new MCP server".

Add the following configuration to `mcp.json`:
```json
{
    "mcpServers": {
      "financial-mcp-server": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "ghcr.io/juannpmari/stockanalyzermcp"
      ]
    }
  }
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

## Available Tools

| Tool                         | Description                                                                                                   |
|------------------------------|---------------------------------------------------------------------------------------------------------------|
| `search_stock_tickers`       | Returns up to 20 ticker names related to a query.                                                             |
| `list_ticker_news`           | Retrieves recent news about a ticker (customizable count and time window).                                    |
| `get_tickers_price`          | Returns the current price for one or more tickers.                                                            |
| `get_historical_prices`      | Provides historical Open, High, Low, Close, and Volume data for a ticker over a specified date range.         |
| `fetch_fundamentals`         | Returns Market Cap, PE Ratio, EPS, Revenue, and Earnings for a ticker (fundamental analysis).                 |
| `fetch_earnings_dates`       | Returns upcoming earnings announcement dates for a ticker (fundamental analysis).                             |
| `fetch_technical_indicators` | Returns technical indicators (SMA, EMA, RSI, MACD, Bollinger Bands) for a ticker (technical analysis).        |



## License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](LICENSE) file for more details.