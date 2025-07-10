import requests

def list_ticker_news(ticker: str, n_news: int = 10, hours_ago: int = 0) -> str:
    """ Returns n_news news about a ticker from the last hours_ago hours. Use to get context to predict ticker evolution.
    
    Parameters:
    ticker (str): e.g. 'AAPL' or 'GOOG', 'MSFT'
    n_news (int): number of news to return
    hours_ago (int): news are from up to hours_ago hours ago

    Returns:
    str: string with the last n_news news about the ticker
    """
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