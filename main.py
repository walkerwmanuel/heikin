import asyncio
import json
from services.info import getCandles , getCandleSnapshot # Import from services folder
from logic.candle import convertToHeikinAshi
from logic.algo import buyWithTrend

if __name__ == "__main__":

    # Websocket logic
    # asyncio.run(getCandles("SUI", "4h"))  # Run the WebSocket function

    # REST API logic
    # Get the last 5000 5m candles for SUI
    candles = getCandleSnapshot('SUI', '5m')
    heikinAshiCandles = convertToHeikinAshi(candles)
    totalCash = buyWithTrend(heikinAshiCandles, candles)
    print(totalCash)
    # Print first 5 candles for reference