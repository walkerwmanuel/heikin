import asyncio
import json
from services.info import getCandles , getCandleSnapshot # Import from services folder
from logic.candle import convertToHeikinAshi
from logic.algo import longAllHeikinGreen, shortAllHeikinRed, shortInHighVol
from logic.volume import calculateVWAPOfCandles

if __name__ == "__main__":

    # Websocket logic
    # asyncio.run(getCandles("SUI", "4h"))  # Run the WebSocket function

    # REST API logic
    # Get the last 5000 5m candles for SUI
    candles = getCandleSnapshot('SUI', '5m')
    # print(json.dumps(candles, indent=4))

    # vwap30Minutes = calculateVWAPOfCandles(candles[-6:])
    # print(vwap30Minutes)

    heikinAshiCandles = convertToHeikinAshi(candles)

    # totalCash = longAllHeikinGreen(heikinAshiCandles, candles, 1000)
    totalCashFromShort = shortAllHeikinRed(heikinAshiCandles, candles, 1000, 1)
    print(totalCashFromShort)

    totalCashHighVolShort = shortInHighVol(heikinAshiCandles, candles, 1000, 1)
    print(totalCashHighVolShort)