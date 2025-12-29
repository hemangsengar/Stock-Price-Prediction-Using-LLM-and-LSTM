import yfinance as yf
import pandas as pd
import anthropic
import os
import asyncio
import numpy as np
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from pydantic import BaseModel, Field
from typing import List, Optional

# Load API Key
load_dotenv()
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.AsyncAnthropic(api_key=CLAUDE_API_KEY)

# === Structured Data Models ===
class TechnicalIndicators(BaseModel):
    rsi: float
    sma50: float
    ema20: float
    macd: float
    macd_signal: float

class NewsItem(BaseModel):
    title: str
    link: str
    sentiment_impact: Optional[str] = None

class PeerInfo(BaseModel):
    ticker: str
    price: float
    pe: Optional[float] = None
    change_pct: float

class AnalysisReport(BaseModel):
    ticker: str
    company_name: str
    latest_price: float
    lstm_trend: str
    news_sentiment_score: float = Field(..., description="Score from -1 to 1 based on news headlines")
    unified_alpha_score: float = Field(..., description="Aggregated confidence score from 0-100")
    recommendation: str
    key_headlines: List[NewsItem]
    claude_summary: str
    business_summary: Optional[str] = None
    indicators: TechnicalIndicators
    peers: List[PeerInfo] = []
    sector_pe_avg: Optional[float] = None

# === News Scraper (Async) ===
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

# === Claude Utilities (Async) ===
async def get_nse_ticker_from_name(company_name):
    system_prompt = f"""
You are a stock market expert. Given a company name, return its NSE stock symbol with '.NS' at the end. 
Reply only with the symbol (like INFY.NS, TCS.NS, etc.). If unknown, say 'NOT_FOUND'.
Company Name: {company_name}
"""
    try:
        print(f"🔍 Looking up ticker for: {company_name}")
        message = await client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=20,
            messages=[{"role": "user", "content": system_prompt}]
        )
        symbol = message.content[0].text.strip()
        
        # Validation
        if symbol.endswith(".NS") and ticker_exists(symbol):
            print(f"✅ AI returned valid symbol: {symbol}")
            return symbol
            
        print(f"⚠️ AI returned symbol '{symbol}' is invalid or unknown. Falling back to search...")
    except Exception as e:
        print(f"❌ AI Ticker lookup error: {e}")

    # Fallback: Ticker Search
    return search_ticker_fallback(company_name)

def ticker_exists(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return not data.empty
    except:
        return False

async def get_sector_peers(ticker):
    """
    Uses Claude to identify top 3 NSE competitors for the given ticker.
    """
    system_prompt = f"""
You are a financial analyst. Identify the TOP 3 direct competitors of the company {ticker} that are listed on the National Stock Exchange (NSE) of India.
Return ONLY their NSE tickers with '.NS' suffix, comma-separated (e.g., 'TCS.NS,WIPRO.NS,HCLTECH.NS').
Do not include {ticker} itself. If unknown, return 'NOT_FOUND'.
"""
    try:
        message = await client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=50,
            messages=[{"role": "user", "content": system_prompt}]
        )
        tickers = message.content[0].text.strip().split(',')
        peer_list = [t.strip() for t in tickers if t.strip().endswith(".NS")]
        print(f"👥 Identified peers: {peer_list}")
        return peer_list
    except Exception as e:
        print(f"Peer identification error: {e}")
        return []

async def fetch_peer_data(ticker):
    """
    Fetches key metrics for a single peer.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="2d")
        
        change_pct = 0.0
        if len(hist) >= 2:
            prev_close = hist['Close'].iloc[-2]
            curr_close = hist['Close'].iloc[-1]
            change_pct = ((curr_close - prev_close) / prev_close) * 100
            
        return PeerInfo(
            ticker=ticker,
            price=float(info.get('currentPrice', 0)),
            pe=info.get('trailingPE'),
            change_pct=float(change_pct)
        )
    except Exception as e:
        print(f"Error fetching data for peer {ticker}: {e}")
        return None

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

# === Technical Indicators ===
def calculate_indicators(df):
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
    
    ema_12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema_26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema_12 - ema_26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))
    return df

# === LSTM Trend Prediction (Internal) ===
def predict_trend_lstm(df, ticker):
    model_path = f"Models/{ticker.replace('.NS', '')}_lstm_model.h5"
    
    # Pre-calculate features needed for both LSTM and Fallback
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    df["Return_21D"] = df["Close"].pct_change(21)
    df["Support_20D"] = df["Close"].rolling(20).min()
    df["Resistance_20D"] = df["Close"].rolling(20).max()
    df.dropna(inplace=True)

    if df.empty:
        print(f"⚠️ Dataframe became empty after dropna for {ticker}. Using base Neutral.")
        return "Neutral"

    if not os.path.exists(model_path):
        print(f"ℹ️ Model not found for {ticker}. Using technical heuristic...")
        return get_technical_trend_fallback(df.iloc[-1])

    features = ['RSI_14', 'SMA_50', 'MACD', 'MACD_Signal', 'MACD_Hist', 'Return_21D', 'Support_20D', 'Resistance_20D', 'Volume']
    recent_data = df[features].tail(60)
    if recent_data.shape[0] < 60: 
        return get_technical_trend_fallback(df.iloc[-1])

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(recent_data)
    X_input = np.expand_dims(scaled, axis=0)

    try:
        model = load_model(model_path)
        prediction = model.predict(X_input)
        label_map = {0: "Bullish", 1: "Bearish", 2: "Sideways"}
        return label_map[np.argmax(prediction)]
    except:
        return get_technical_trend_fallback(df.iloc[-1])

def get_technical_trend_fallback(row):
    """
    Fallback: A rule-based trend classifier using RSI and MACD.
    Used when a deep learning model isn't available for a specific ticker.
    """
    try:
        rsi = float(row['RSI_14'])
        macd = float(row['MACD'])
        macd_signal = float(row['MACD_Signal'])
        
        if rsi > 60 and macd > macd_signal:
            return "Bullish (Heuristic)"
        elif rsi < 40 and macd < macd_signal:
            return "Bearish (Heuristic)"
        else:
            return "Sideways (Heuristic)"
    except:
        return "Neutral"

# === Unified Alpha Score Logic ===
def calculate_alpha_score(lstm_trend, news_sentiment):
    """
    Combines LSTM and news sentiment into a 0-100 score.
    """
    # Standardize trend for scoring
    clean_trend = lstm_trend.split(" (")[0]
    trend_scores = {"Bullish": 60, "Sideways": 40, "Bearish": 20, "Unknown": 35, "Neutral": 35}
    base_score = trend_scores.get(clean_trend, 35)
    
    # News sentiment contributes +/- 30 to the base score
    sentiment_contribution = news_sentiment * 30
    
    final_score = base_score + sentiment_contribution
    return max(0, min(100, final_score))

# === AI Analysis (Async) ===
async def get_claude_comprehensive_analysis(ticker, latest, indicators, fundamentals, news, lstm_result):
    news_titles = "\n".join([f"- {n.title}" for n in news])
    prompt = f"""
You are a Quant Analyst. Analyze {ticker} using these inputs:
Price: {float(latest['Close'].iloc[0]) if hasattr(latest['Close'], 'iloc') else float(latest['Close']):.2f}
RSI: {indicators.rsi:.2f}, LSTM Trend: {lstm_result}
Fundamental P/E: {fundamentals['pe']}, Sector: {fundamentals['sector']}
Recent News Headlines:
{news_titles}

CRITICAL: Return ONLY a valid JSON object. No other text.
JSON Schema:
{{
  "sentiment_score": float (-1.0 to 1.0),
  "summary": string (3 sentences),
  "recommendation": "BUY" | "HOLD" | "AVOID",
  "news_impact": string[] (impact description for each news item)
}}
"""
    try:
        message = await client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        content = message.content[0].text
        # Clean potential markdown block
        if content.startswith("```json"):
            content = content[7:-3].strip()
        elif content.startswith("```"):
            content = content[3:-3].strip()
        
        import json
        return json.loads(content)
    except Exception as e:
        print(f"AI parsing error: {e}")
        return {"sentiment_score": 0.0, "summary": "Error parsing AI analysis", "recommendation": "HOLD", "news_impact": []}

# === Main Analysis Engine (Async) ===
async def perform_full_analysis(company_name):
    ticker = await get_nse_ticker_from_name(company_name)
    if ticker == "NOT_FOUND": return {"error": "Ticker not found"}

    try:
        # Step 1: Parallel Data Fetching
        print(f"🚀 Launching async analysis for {ticker}...")
        
        # We wrap blocking yfinance calls in run_in_executor if needed, but here simple async is fine for demonstration
        df_task = asyncio.to_thread(yf.download, ticker, period="12mo", interval="1d", progress=False)
        news_task = get_stock_news(ticker)
        peer_tickers_task = get_sector_peers(ticker)
        
        df, news, peer_tickers = await asyncio.gather(df_task, news_task, peer_tickers_task)
        
        if df.empty: return {"error": "No market data"}

        # Flatten MultiIndex columns if present (yfinance 0.2.0+ behavior)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Step 2: Technicals & LSTM
        df = calculate_indicators(df)
        latest_row = df.iloc[-1]
        
        indicators = TechnicalIndicators(
            rsi=float(latest_row['RSI_14'].iloc[0]) if isinstance(latest_row['RSI_14'], pd.Series) else float(latest_row['RSI_14']),
            sma50=float(latest_row['SMA_50'].iloc[0]) if isinstance(latest_row['SMA_50'], pd.Series) else float(latest_row['SMA_50']),
            ema20=float(latest_row['EMA_20'].iloc[0]) if isinstance(latest_row['EMA_20'], pd.Series) else float(latest_row['EMA_20']),
            macd=float(latest_row['MACD'].iloc[0]) if isinstance(latest_row['MACD'], pd.Series) else float(latest_row['MACD']),
            macd_signal=float(latest_row['MACD_Signal'].iloc[0]) if isinstance(latest_row['MACD_Signal'], pd.Series) else float(latest_row['MACD_Signal'])
        )
        
        info = yf.Ticker(ticker).info
        fundamentals = {"pe": info.get("trailingPE", "N/A"), "sector": info.get("sector", "N/A")}
        business_summary = info.get("longBusinessSummary")
        
        lstm_trend = predict_trend_lstm(df.copy(), ticker)
        
        # Step 3: Peer Analysis (Parallel)
        peer_data_tasks = [fetch_peer_data(t) for t in peer_tickers]
        peers_result = await asyncio.gather(*peer_data_tasks)
        peers = [p for p in peers_result if p is not None]
        
        # Calculate Sector PE Avg
        pe_list = [p.pe for p in peers if p.pe]
        if fundamentals['pe'] != "N/A": pe_list.append(fundamentals['pe'])
        sector_pe_avg = sum(pe_list) / len(pe_list) if pe_list else None

        # Step 4: AI Sentiment Analysis
        ai_data = await get_claude_comprehensive_analysis(ticker, latest_row, indicators, fundamentals, news, lstm_trend)
        
        # Step 5: Alpha Scoring
        alpha_score = calculate_alpha_score(lstm_trend, ai_data['sentiment_score'])

        # Update news objects with impact
        for i, item in enumerate(news):
            if i < len(ai_data.get('news_impact', [])):
                item.sentiment_impact = ai_data['news_impact'][i]

        return AnalysisReport(
            ticker=ticker,
            company_name=company_name,
            latest_price=float(latest_row['Close'].iloc[0]) if isinstance(latest_row['Close'], pd.Series) else float(latest_row['Close']),
            lstm_trend=lstm_trend,
            news_sentiment_score=ai_data['sentiment_score'],
            unified_alpha_score=alpha_score,
            recommendation=ai_data['recommendation'],
            key_headlines=news,
            claude_summary=ai_data['summary'],
            business_summary=business_summary,
            indicators=indicators,
            peers=peers,
            sector_pe_avg=sector_pe_avg
        ).model_dump()

    except Exception as e:
        return {"error": str(e)}

# === CLI Entrypoint ===
if __name__ == "__main__":
    name = input("Enter Company Name: ")
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(perform_full_analysis(name))
    print(res)
