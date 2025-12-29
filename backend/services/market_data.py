import pandas as pd

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
