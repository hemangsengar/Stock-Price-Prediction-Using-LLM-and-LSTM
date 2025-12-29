import asyncio
from core.engine import perform_full_analysis
from services.ai_service import get_nse_ticker_from_name

# Legacy support for CLI and external imports
# This script now acts as a bridge to the modular architecture.

if __name__ == "__main__":
    name = input("Enter Company Name: ")
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(perform_full_analysis(name))
    print(res)
