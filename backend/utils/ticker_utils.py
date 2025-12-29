import yfinance as yf

def ticker_exists(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return not data.empty
    except:
        return False

def search_ticker_fallback(query):
    print(f"🔄 Searching for ticker: {query}")
    try:
        # We use yfinance search results
        search_results = yf.Search(query).quotes
        for result in search_results:
            symbol = result.get('symbol', '')
            # Prioritize NSE stocks
            if symbol.endswith(".NS"):
                print(f"🎯 Found NSE match in search: {symbol}")
                return symbol
        
        # If no NSE match, return the first symbol if it exists
        if search_results:
            symbol = search_results[0].get('symbol', '')
            print(f"💡 Found alternative symbol in search: {symbol}")
            return symbol
            
    except Exception as e:
        print(f"❌ Search fallback failed: {e}")
    
    return "NOT_FOUND"
