from typing import List, Dict
import yfinance as yf
import pandas as pd
import requests


def search_stock_tickers(ticker_query: str = "") -> Dict[str, str]:
    try:
        ticker_query = ticker_query.lower()
        url = "https://api.tickertick.com/tickers"
        params = {
            "p": f"{ticker_query}",
            "n": 20,
        }

        response = requests.get(url, params=params)
        data = response.json()

        return {item["ticker"]: item["company_name"] for item in data["tickers"]}
    except Exception as e:
        return {"error": str(e)}


def list_ticker_news(
    ticker: str, n_news: int = 10, hours_ago: int = 0
) -> Dict[str, str]:
    try:
        ticker = ticker.lower()
        url = "https://api.tickertick.com/feed"
        params = {
            "q": f"(and tt:{ticker} T:curated)",
            "n": n_news,
            "hours_ago": hours_ago,
        }

        response = requests.get(url, params=params)
        data = response.json()

        news = f"Last {n_news} news about {ticker}: \n"
        for item in data["stories"]:
            news += f" Title: {item['title']} \n"
            if "description" in item:
                news += f" Description: {item['description']} \n"
            news += f" URL: {item['url']} \n"
            news += "--------------------------------\n"

        return {"news": news}
    except Exception as e:
        return {"error": str(e)}


def get_tickers_price(tickers: list[str]) -> Dict[str, float]:
    try:
        prices = {}
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                price = stock.info["regularMarketPrice"]
                prices[ticker] = price
            except Exception as e:
                prices[ticker] = f"Error: {e}"
        return prices
    except Exception as e:
        return {"error": str(e)}


def get_historical_prices(
    ticker: str, start_date: str, end_date: str, interval: str = "1d"
) -> List[tuple]:
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
