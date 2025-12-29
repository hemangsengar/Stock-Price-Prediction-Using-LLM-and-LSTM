from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from stock_analysis import perform_full_analysis, get_nse_ticker_from_name
from cache_manager import cache
import os
import asyncio

app = FastAPI(title="StockPulse Advanced API")

# Setup templates and static files
os.makedirs('static/css', exist_ok=True)
os.makedirs('templates', exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class AnalysisRequest(BaseModel):
    company_name: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze(data: AnalysisRequest):
    if not data.company_name:
        raise HTTPException(status_code=400, detail="Company name is required")
    
    # Check if we can resolve the ticker first to use as a cache key
    ticker = await get_nse_ticker_from_name(data.company_name)
    if ticker == "NOT_FOUND":
        return {"error": "Ticker not found for this company"}

    # Caching Layer check
    cached_result = cache.get(ticker)
    if cached_result and "peers" in cached_result:
        print(f"✅ Cache Hit for {ticker}")
        return cached_result
    elif cached_result:
        print(f"🔄 Stale cache found (missing Peer data) for {ticker}. Re-running analysis...")

    # Async Analysis
    result = await perform_full_analysis(data.company_name)
    
    # Conditional Caching: Only cache if analysis was truly successful
    if "error" not in result:
        trend = result.get("lstm_trend", "")
        alpha = result.get("unified_alpha_score", 0)
        print(f"📊 Analysis Result for {ticker}: Trend={trend}, Alpha={alpha}")
        
        # Don't cache if we still have Unknown for some reason
        if "Unknown" not in trend:
            cache.set(ticker, result)
            print(f"💾 Results cached for {ticker}")
        else:
            print(f"⚠️ Result contains 'Unknown' trend. Skipping cache.")
        
    return result

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting StockPulse API on http://127.0.0.1:8080")
    uvicorn.run(app, host="127.0.0.1", port=8080)
