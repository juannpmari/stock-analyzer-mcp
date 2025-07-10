
from mcp.server.fastmcp import FastMCP
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

if __name__ == "__main__":
    mcp.run(transport="stdio")