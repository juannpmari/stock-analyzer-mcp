from mcp.server.fastmcp import FastMCP
from typing import Dict, Union
from tools import market_data, analysis

mcp = FastMCP("Market analyzer")


@mcp.tool()
def search_stock_tickers(ticker_query: str = "") -> Dict[str, str]:
    """Return up to 20 ticker names related to ticker_query. Use to retrieve tickers names for other resources.
    Parameters:
    ticker_query (str): e.g. 'AAPL' or 'GOOG', 'MSFT'

    Returns:
    Dict[str, str]: Dictionary with tickers as keys and their company names as values.
    """
    return market_data.search_stock_tickers(ticker_query)


@mcp.tool()
def list_ticker_news(
    ticker: str, n_news: int = 10, hours_ago: int = 0
) -> Dict[str, str]:
    """Returns n_news news about a ticker from the last hours_ago hours. Use to get context to predict ticker evolution.

    Parameters:
    ticker (str): e.g. 'AAPL' or 'GOOG'
    n_news (int): number of news to return
    hours_ago (int): number of hours ago to get news from

    Returns:
    Dict[str, str]: Dictionary with news as keys and their titles as values.
    """
    return market_data.list_ticker_news(ticker, n_news, hours_ago)


@mcp.tool()
def get_tickers_price(tickers: list[str]) -> Dict[str, str]:
    """Returns the price of a list of tickers.

    Parameters:
    tickers (list[str]): list of tickers to get price from

    Returns:
    Dict[str, float]: Dictionary with tickers as keys and their prices as values.
    """
    return market_data.get_tickers_price(tickers)


@mcp.tool()
def get_historical_prices(
    ticker: str, start_date: str, end_date: str, interval: str = "1d"
) -> Dict[str, Union[tuple, str]]:
    """
    Fetches daily closing prices for a given ticker between start_date and end_date.

    Parameters:
    - ticker (str): e.g. 'AAPL' or 'BTC-USD'
    - start_date (str): e.g. '2024-01-01'
    - end_date (str): e.g. '2024-06-01'
    - interval (str): e.g. '1d', '1h', '1m'

    Returns:
    - List of (date, open, high, low, close, volume) tuples
    - If the ticker is not found, returns an empty list
    """
    return market_data.get_historical_prices(ticker, start_date, end_date, interval)


@mcp.tool()
def fetch_fundamentals(ticker_id: str) -> Dict[str, str]:
    """
    Fetches fundamental data for a given ticker.

    Parameters:
    ticker_id (str): e.g. 'AAPL' or 'GOOG'

    Returns:
    dict: Dictionary with Market Cap, PE Ratio, EPS, Revenue, and Earnings.
    """
    return analysis.fetch_fundamentals(ticker_id)


@mcp.tool()
def fetch_earnings_dates(ticker_id: str) -> Dict[str, str]:
    """
    Fetches upcoming earnings announcement dates for a given ticker.

    Parameters:
    ticker_id (str): e.g. 'AAPL' or 'GOOG'

    Returns:
    dict: Dictionary with earnings dates and related information.
    """
    return analysis.fetch_earnings_dates(ticker_id)


@mcp.tool()
def fetch_technical_indicators(ticker: str, start: str, end: str) -> Dict[str, str]:
    """Returns an analysis of a ticker.

    Parameters:
    ticker (str): e.g. 'AAPL' or 'GOOG'

    Returns:
    Dict[str, str]: Dictionary with analysis as keys and their titles as values.
    """
    return analysis.fetch_technical_indicators(ticker, start, end)


if __name__ == "__main__":
    mcp.run(transport="stdio")
