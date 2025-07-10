import yfinance as yf
from typing import Dict


def get_technical_indicators(ticker, start, end) -> Dict[str, float]:
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
        print(f"Error fetching indicators for {ticker}: {e}")
        return None
