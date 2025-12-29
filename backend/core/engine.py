import asyncio
import yfinance as yf
import pandas as pd
from data_models.schemas import AnalysisReport, TechnicalIndicators
from services.market_data import calculate_indicators, calculate_alpha_score
from services.news_service import get_stock_news
from services.ml_service import predict_trend_lstm
from services.ai_service import (
    get_nse_ticker_from_name, 
    get_sector_peers, 
    fetch_peer_data, 
    get_claude_comprehensive_analysis
)
from utils.ticker_utils import search_ticker_fallback

async def perform_full_analysis(company_name: str):
    """
    Modular orchestrator for stock analysis.
    """
    try:
        # Step 1: Resolve Ticker
        ticker = await get_nse_ticker_from_name(company_name)
        if ticker == "NOT_FOUND":
            ticker = search_ticker_fallback(company_name)
            if ticker == "NOT_FOUND":
                return {"error": "Could not find a valid NSE ticker for this company."}

        print(f"🚀 Launching modular analysis for {ticker}...")
        
        # Step 2: Parallel Data Acquisition
        # We fetch historical data, news, and peer list concurrently
        df_task = asyncio.to_thread(yf.download, ticker, period="2y", interval="1d", progress=False)
        news_task = get_stock_news(ticker)
        peer_tickers_task = get_sector_peers(ticker)
        
        df, news, peer_tickers = await asyncio.gather(df_task, news_task, peer_tickers_task)

        if df.empty:
            return {"error": f"No market data found for {ticker}"}

        # Flatten columns if MultiIndex (yfinance 0.2.40+ change)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Calculate Technicals
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
        
        # ML Trend Prediction
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

        # Final Report
        report = AnalysisReport(
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
        )
        
        return report.model_dump()

    except Exception as e:
        print(f"Analysis engine error: {e}")
        return {"error": str(e)}
