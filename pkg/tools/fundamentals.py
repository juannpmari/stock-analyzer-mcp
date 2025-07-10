import yfinance as yf


def fundamentals(ticker_id: str) -> dict:
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

def earnings_dates(ticker_id: str) -> dict:
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
