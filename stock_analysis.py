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
    indicators: TechnicalIndicators

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
        print(f"✅ AI returned symbol: {symbol}")
        return symbol if symbol.endswith(".NS") else "NOT_FOUND"
    except Exception as e:
        print(f"❌ AI Ticker lookup error: {e}")
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
    if not os.path.exists(model_path):
        return "Unknown"

    # Reuse indicator logic for LSTM features
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    df["Return_21D"] = df["Close"].pct_change(21)
    df["Support_20D"] = df["Close"].rolling(20).min()
    df["Resistance_20D"] = df["Close"].rolling(20).max()
    df.dropna(inplace=True)

    features = ['RSI_14', 'SMA_50', 'MACD', 'MACD_Signal', 'MACD_Hist', 'Return_21D', 'Support_20D', 'Resistance_20D', 'Volume']
    recent_data = df[features].tail(60)
    if recent_data.shape[0] < 60: return "Unknown"

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(recent_data)
    X_input = np.expand_dims(scaled, axis=0)

    try:
        model = load_model(model_path)
        prediction = model.predict(X_input)
        label_map = {0: "Bullish", 1: "Bearish", 2: "Sideways"}
        return label_map[np.argmax(prediction)]
    except:
        return "Unknown"

# === Unified Alpha Score Logic ===
def calculate_alpha_score(lstm_trend, news_sentiment):
    """
    Combines LSTM and news sentiment into a 0-100 score.
    """
    trend_scores = {"Bullish": 60, "Sideways": 40, "Bearish": 20, "Unknown": 35}
    base_score = trend_scores.get(lstm_trend, 35)
    
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
        df = yf.download(ticker, period="12mo", interval="1d", progress=False)
        news_task = get_stock_news(ticker)
        
        news = await news_task
        
        if df.empty: return {"error": "No market data"}

        # Step 2: Technicals & LSTM
        df = calculate_indicators(df)
        latest_row = df.iloc[-1]
        
        indicators = TechnicalIndicators(
            rsi=float(latest_row['RSI_14']),
            sma50=float(latest_row['SMA_50']),
            ema20=float(latest_row['EMA_20']),
            macd=float(latest_row['MACD']),
            macd_signal=float(latest_row['MACD_Signal'])
        )
        
        info = yf.Ticker(ticker).info
        fundamentals = {"pe": info.get("trailingPE", "N/A"), "sector": info.get("sector", "N/A")}
        
        lstm_trend = predict_trend_lstm(df.copy(), ticker)
        
        # Step 3: AI Sentiment Analysis
        ai_data = await get_claude_comprehensive_analysis(ticker, latest_row, indicators, fundamentals, news, lstm_trend)
        
        # Step 4: Alpha Scoring
        alpha_score = calculate_alpha_score(lstm_trend, ai_data['sentiment_score'])

        # Update news objects with impact
        for i, item in enumerate(news):
            if i < len(ai_data.get('news_impact', [])):
                item.sentiment_impact = ai_data['news_impact'][i]

        return AnalysisReport(
            ticker=ticker,
            company_name=company_name,
            latest_price=float(latest_row['Close']),
            lstm_trend=lstm_trend,
            news_sentiment_score=ai_data['sentiment_score'],
            unified_alpha_score=alpha_score,
            recommendation=ai_data['recommendation'],
            key_headlines=news,
            claude_summary=ai_data['summary'],
            indicators=indicators
        ).model_dump()

    except Exception as e:
        return {"error": str(e)}

# === CLI Entrypoint ===
if __name__ == "__main__":
    name = input("Enter Company Name: ")
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(perform_full_analysis(name))
    print(res)
