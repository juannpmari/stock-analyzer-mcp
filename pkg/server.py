
from typing import List, Dict
from mcp.server.fastmcp import FastMCP
import yfinance as yf
import pandas as pd
import requests
from tools.basic import search_stock_tickers, get_tickers_price, get_historical_prices
from tools.fundamentals import fundamentals, earnings_dates
from tools.news import list_ticker_news

mcp = FastMCP("Market analyzer")


mcp.tool()(fundamentals)
mcp.tool()(earnings_dates)
mcp.tool()(search_stock_tickers)
mcp.tool()(get_tickers_price)
mcp.tool()(get_historical_prices)
mcp.tool()(list_ticker_news)

@mcp.prompt()
def summarize_ticker_news(ticker: str, news: List[str] = []) -> str:
    """
    """
    return f"Given the following news about {ticker}: {news}, summarize them in a single paragraph."


# Run the server
if __name__ == "__main__":
    mcp.run(transport="stdio")