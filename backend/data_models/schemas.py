from pydantic import BaseModel, Field
from typing import List, Optional

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
