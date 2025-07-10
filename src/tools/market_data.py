from typing import List, Dict
import yfinance as yf
import pandas as pd
import requests
from mcp.server.fastmcp import FastMCP

market_data_mcp = FastMCP("Market Data")


@market_data_mcp.tool   
def search_stock_tickers(ticker_query: str = "") -> Dict[str, str]:
    """Return up to 20 ticker names related to ticker_query. Use to retrieve tickers names for other resources.
    
    Parameters:
    ticker_query (str): e.g. 'AAPL' or 'GOOG', 'MSFT'
    
    Returns:
    Dict[str, str]: Dictionary with tickers as keys and their company names as values.
    """
    try:
        ticker_query = ticker_query.lower()
        url = "https://api.tickertick.com/tickers"
        params = {
            "p": f"{ticker_query}",
            "n": 20,
        }

        response = requests.get(url, params=params)
        data = response.json()

        return {item['ticker']:item['company_name'] for item in data['tickers']}
    except Exception as e:
        return {"error": str(e)}


@market_data_mcp.tool
def list_ticker_news(ticker: str, n_news: int = 10, hours_ago: int = 0) -> Dict[str, str]:
    """ Returns n_news news about a ticker from the last hours_ago hours. Use to get context to predict ticker evolution.
    
    Parameters:
    ticker (str): e.g. 'AAPL' or 'GOOG', 'MSFT'
    n_news (int): number of news to return
    hours_ago (int): news are from up to hours_ago hours ago

    Returns:
    Dict[str, str]: Dictionary with news as keys and their company names as values.
    """
    try:
        ticker = ticker.lower()
        url = "https://api.tickertick.com/feed"
        params = {
            "q": f"(and tt:{ticker} T:curated)",
            "n": n_news,
            "hours_ago": hours_ago
        }

        response = requests.get(url, params=params)
        data = response.json()

        news=f"Last {n_news} news about {ticker}: \n"
        for item in data["stories"]:
            news += f" Title: {item['title']} \n"
            if 'description' in item:
                news += f" Description: {item['description']} \n"
            news += f" URL: {item['url']} \n"
            news += "--------------------------------\n"

        return news
    except Exception as e:
        return {"error": str(e)}

@market_data_mcp.tool
def get_tickers_price(tickers: list[str]) -> Dict[str, float]:
    """
    Get the latest price for a list of tickers using yfinance.

    Parameters:
    tickers (list): List of ticker symbols (e.g., ['AAPL', 'GOOG', 'MSFT'])

    Returns:
    Dict[str, float]: Dictionary with tickers as keys and their latest price as values.
    """
    try:
        prices = {}
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                price = stock.info['regularMarketPrice']
                prices[ticker] = price
            except Exception as e:
                prices[ticker] = f"Error: {e}"
        return prices
    except Exception as e:
        return {"error": str(e)}

@market_data_mcp.tool
def get_historical_prices(ticker: str, start_date: str, end_date: str, interval: str = "1d") -> List[tuple]:
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
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date, interval=interval)
        if data.empty:
            return []

        data = data.reset_index()

        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        return [
            (str(date.date()), open_price, high, low, close, volume)
            for date, open_price, high, low, close, volume in zip(
                dates,
                data["Open"],
                data["High"],
                data["Low"],
                data["Close"],
                data["Volume"],
            )
        ]

    except Exception as e:
        return {"error": str(e)}
