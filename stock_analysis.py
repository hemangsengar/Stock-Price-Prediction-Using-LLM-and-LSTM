import yfinance as yf
import pandas as pd
import anthropic
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# === Technical Indicator Calculations ===
def calculate_sma(df, period=50):
    df[f"SMA_{period}"] = df["Close"].rolling(window=period).mean()

def calculate_ema(df, period=20):
    df[f"EMA_{period}"] = df["Close"].ewm(span=period, adjust=False).mean()

def calculate_macd(df):
    ema_12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema_26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema_12 - ema_26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

def calculate_rsi(df, period=14):
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))

# === Trend Classification Logic ===
def classify_trend(df):
    latest = df.iloc[-1]
    rsi = latest["RSI_14"].item()
    close = latest["Close"].item()
    sma_50 = latest["SMA_50"].item()
    macd = latest["MACD"].item()
    macd_signal = latest["MACD_Signal"].item()

    is_bullish = rsi > 60 and close > sma_50 and macd > macd_signal
    is_bearish = rsi < 40 and close < sma_50 and macd < macd_signal

    if is_bullish:
        return "Bullish"
    elif is_bearish:
        return "Bearish"
    else:
        return "Sideways / Neutral"

# === Claude Prompt Builder ===
def build_claude_prompt(ticker, latest, pe, eps, sector, LSTM_Result):
    return f"""
You are a professional stock market analyst. Based on the following indicators and fundamentals for stock **{ticker}** (Use the Public Known Name of the company) and I am giving you the LSTM Model result {LSTM_Result}, write a short report.

Technical Indicators:
- Close Price: Rs.{latest['Close'].item():.2f}
- RSI (14): {latest['RSI_14'].item():.2f}
- SMA (50): Rs.{latest['SMA_50'].item():.2f}
- EMA (20): Rs.{latest['EMA_20'].item():.2f}
- MACD: {latest['MACD'].item():.2f}
- MACD Signal: {latest['MACD_Signal'].item():.2f}

Fundamentals:
- Sector: {sector}
- P/E Ratio: {pe}
- EPS (TTM): Rs.{eps}

Please provide:
1. A 1-line summary of the indicators (Giving full name of the indicators) and also the recent real challenges faced by the company.
2. The current price of the stock and the trend (bullish/bearish/sideways) and why (use the {LSTM_Result} from the LSTM model for the explanation.).
3. Also provide what Various Research Agencies are having its outloop towards the stock price target weather to buy sell or hold.
4. Market or sector-level trend that could affect this stock, and the recent real challenges faced by the company.
5. Investor recommendation (buy/hold/avoid) with explanation and sentiments.
Tone: Clear, confident, and suitable for retail investors.


"""

def get_claude_analysis(prompt):
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=700,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text



import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def predict_trend_lstm(df, ticker):
    # Recalculate required indicators
    df["SMA_50"] = df["Close"].rolling(window=50).mean()
    ema_12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema_26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema_12 - ema_26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    df["RSI_14"] = 100 - (100 / (1 + (
        df["Close"].diff().clip(lower=0).rolling(14).mean() /
        (-df["Close"].diff().clip(upper=0).rolling(14).mean())
    )))
    df["Return_21D"] = df["Close"].pct_change(21)
    df["Support_20D"] = df["Close"].rolling(20).min()
    df["Resistance_20D"] = df["Close"].rolling(20).max()

    df.dropna(inplace=True)

    features = [
        'RSI_14', 'SMA_50', 'MACD', 'MACD_Signal', 'MACD_Hist',
        'Return_21D', 'Support_20D', 'Resistance_20D', 'Volume'
    ]
    recent_data = df[features].tail(60)
    if recent_data.shape[0] < 60:
        return "Insufficient data for LSTM prediction."

    # Scale
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(recent_data)
    X_input = np.expand_dims(scaled, axis=0)

    # Load model
    model_path = f"Models/{ticker.replace('.NS', '')}_lstm_model.h5"
    model = load_model(model_path)

    # Predict
    prediction = model.predict(X_input)
    label_map = {0: "Bullish", 1: "Bearish", 2: "Sideways"}
    predicted_class = np.argmax(prediction)
    return label_map[predicted_class]


# === Main Program ===
if __name__ == "__main__":
    ticker = input("Enter NSE stock symbol (e.g., INFY.NS, TCS.NS): ").strip().upper()

    try:
        print("Fetching data...")
        df = yf.download(ticker, period="12mo", interval="1d")
        if df.empty:
            raise ValueError("No data retrieved.")

        calculate_sma(df)
        calculate_ema(df)
        calculate_macd(df)
        calculate_rsi(df)

        df.dropna(inplace=True)
        latest = df.iloc[-1]

        # Get fundamentals
        print("Fetching fundamentals...")
        info = yf.Ticker(ticker).info
        pe = info.get("trailingPE", "N/A")
        eps = info.get("trailingEps", "N/A")
        sector = info.get("sector", "N/A")

        # Classify trend
        trend = predict_trend_lstm(df, ticker)
        LSTM_Result = print(f"LSTM Trend Prediction: {trend}")


        # Claude Summary
        print("Asking Claude for natural language analysis...")
        prompt = build_claude_prompt(ticker, latest, pe, eps, sector, LSTM_Result)
        summary = get_claude_analysis(prompt)

        print("\nStock Trend Summary:\n")
        print(summary)

    except Exception as e:
        print(f"Error: {e}")