import yfinance as yf
from typing import Dict
from mcp.server.fastmcp import FastMCP

analysis_mcp = FastMCP("Analysis")

@analysis_mcp.tool()
def fetch_fundamentals(ticker_id: str) -> Dict[str, float]:
    """
    Fetches fundamental data for a given ticker.

    Parameters:
    ticker_id (str): e.g. 'AAPL' or 'GOOG'

    Returns:
    dict: Dictionary with Market Cap, PE Ratio, EPS, Revenue, and Earnings.
    """
    try:
        ticker = yf.Ticker(ticker_id)
        info = ticker.info

        fundamentals_data = {
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "revenue": info.get("totalRevenue"),
            "earnings": info.get("grossProfits")
        }

        return fundamentals_data

    except Exception as e:
        return {"error": str(e)}

@analysis_mcp.tool()
def fetch_earnings_dates(ticker_id: str) -> dict:
    """
    Fetches upcoming earnings announcement dates for a given ticker.

    Parameters:
    ticker_id (str): e.g. 'AAPL' or 'GOOG'

    Returns:
    dict: Dictionary with earnings dates and related information.
    """
    try:
        ticker = yf.Ticker(ticker_id)
        calendar = ticker.earnings_dates

        if calendar is None or calendar.empty:
            calendar = ticker.calendar

        if calendar is not None and not calendar.empty:
            earnings_dict = calendar.to_dict()
            return earnings_dict
        else:
            return {"message": "No earnings calendar data available."}

    except Exception as e:
        return {"error": str(e)}



@analysis_mcp.tool()
def fetch_technical_indicators(ticker: str, start: str, end: str) -> Dict[str, float]:
    """
    Fetches technical indicators for a ticker using yfinance and pandas.

    Parameters:
    - ticker (str): e.g., 'AAPL' or 'BTC-USD'
    - start (str): start date in YYYY-MM-DD
    - end (str): end date in YYYY-MM-DD

    Returns:
    - Dictionary with indicators (latest values only)

    """
    try:

        stock = yf.Ticker(ticker)
        data = stock.history(start=start, end=end, interval="1d")
        if data.empty:
            return []

        data = data.reset_index()

        # Calculate Simple Moving Average (SMA)
        data["SMA_20"] = data["Close"].rolling(window=20).mean()

        # Calculate Exponential Moving Average (EMA)
        data["EMA_20"] = data["Close"].ewm(span=20).mean()

        # Calculate RSI (Relative Strength Index)
        def calculate_rsi(prices, period=14):
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi

        data["RSI_14"] = calculate_rsi(data["Close"])

        # Calculate MACD (Moving Average Convergence Divergence)
        ema_12 = data["Close"].ewm(span=12).mean()
        ema_26 = data["Close"].ewm(span=26).mean()
        data["MACD_12_26_9"] = ema_12 - ema_26
        data["MACDs_12_26_9"] = data["MACD_12_26_9"].ewm(span=9).mean()  # Signal line
        data["MACDh_12_26_9"] = (
            data["MACD_12_26_9"] - data["MACDs_12_26_9"]
        )  # Histogram

        # Calculate Bollinger Bands
        data["BBM_20_2.0"] = (
            data["Close"].rolling(window=20).mean()
        )  # Middle band (SMA)
        bb_std = data["Close"].rolling(window=20).std()
        data["BBU_20_2.0"] = data["BBM_20_2.0"] + (bb_std * 2)  # Upper band
        data["BBL_20_2.0"] = data["BBM_20_2.0"] - (bb_std * 2)  # Lower band

        # Return latest row with indicators
        indicators = data.iloc[-1][
            [
                "SMA_20",
                "EMA_20",
                "RSI_14",
                "MACD_12_26_9",
                "MACDh_12_26_9",
                "MACDs_12_26_9",
                "BBL_20_2.0",
                "BBM_20_2.0",
                "BBU_20_2.0",
            ]
        ]

        return indicators.dropna().to_dict()

    except Exception as e:
        return {"error": str(e)}
