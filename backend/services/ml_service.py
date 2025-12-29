import os
import pathlib
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

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

def predict_trend_lstm(df, ticker):
    # Make path absolute relative to this file's parent's parent (backend root)
    backend_root = pathlib.Path(__file__).parent.parent
    model_path = os.path.join(backend_root, "Models", f"{ticker.replace('.NS', '')}_lstm_model.h5")
    
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
