import asyncio
import json
from services.info import getCandles , getCandleSnapshot # Import from services folder
from logic.candle import convertToHeikinAshi
from logic.algo import longAllHeikinGreen, shortAllHeikinRed, shortInHighVol, shortAndLongAllHeikin, fifteenAndTwelve
from logic.volume import calculateVWAPOfCandles

if __name__ == "__main__":

    # Websocket logic
    # asyncio.run(getCandles("SUI", "5m"))  # Run the WebSocket function

    # # REST API logic
    # # Get the last 5000 5m candles for SUI
    # candles = getCandleSnapshot('LTC', '5m')
    # fourHourCandles = getCandleSnapshot('LTC', '4h')
    dayCandles = getCandleSnapshot('SOL', '12h')
    # # print(json.dumps(candles, indent=4))

    # # vwap30Minutes = calculateVWAPOfCandles(candles[-6:])
    # # print(vwap30Minutes)

    # heikinAshiCandles = convertToHeikinAshi(candles)
    # fourHourheikinAshiCandles = convertToHeikinAshi(fourHourCandles)
    dayHeikinAshiCandles = convertToHeikinAshi(dayCandles)

    # # totalCash = longAllHeikinGreen(heikinAshiCandles, candles, 1000)
    # # totalCashFromShort = shortAllHeikinRed(heikinAshiCandles, candles, 1000, 1)
    # # print(totalCashFromShort)

    # # totalCashHighVolShort = shortInHighVol(heikinAshiCandles, candles, 1000, 1)
    # # print(totalCashHighVolShort)

    # totalCash = longAllHeikinGreen(dayHeikinAshiCandles, dayCandles, 1000, 1)
    # totalCash2 = shortAllHeikinRed(dayHeikinAshiCandles, dayCandles, 1000, 1)
    # print(totalCash)
    # print(totalCash2)

    # totalCash = shortAndLongAllHeikin(dayHeikinAshiCandles, dayCandles, 1000, 2)
    # print(totalCash)


    fifteenMC = getCandleSnapshot('SOL', '15m')
    fifteenMHACandles = convertToHeikinAshi(fifteenMC)
    twelveHC = getCandleSnapshot('SOL', '12h')
    twelveHHACandles = convertToHeikinAshi(twelveHC)
    _ = fifteenAndTwelve(fifteenMHACandles, fifteenMC , twelveHHACandles, 1000, 1)