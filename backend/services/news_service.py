import yfinance as yf
from data_models.schemas import NewsItem

async def get_stock_news(ticker):
    """
    Fetches recent news headlines for the stock using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        results = []
        for item in news[:5]:
            content = item.get('content', {})
            results.append(NewsItem(
                title=content.get('title', 'No Title'),
                link=content.get('canonicalUrl', {}).get('url', '')
            ))
        return results
    except Exception as e:
        print(f"Error fetching news for {ticker}: {e}")
        return []
