# Will take in any number of candles and return the heikin ashi candle form.
def convertToHeikinAshi(candles):
    heikinAshiCandles = []

    for i, candle in enumerate(candles):
        openPrice = float(candle["o"])
        highPrice = float(candle["h"])
        lowPrice = float(candle["l"])
        closePrice = float(candle["c"])

        # Calculate HA Close
        haClose = (openPrice + highPrice + lowPrice + closePrice) / 4

        # Calculate HA Open (special case for first candle)
        if i == 0:
            haOpen = openPrice  # First HA open = first regular open
        else:
            haOpen = (heikinAshiCandles[i - 1]["haOpen"] + heikinAshiCandles[i - 1]["haClose"]) / 2

        # Calculate HA High & HA Low
        haHigh = max(highPrice, haOpen, haClose)
        haLow = min(lowPrice, haOpen, haClose)

        # Store Heikin-Ashi candle
        haCandle = {
            "t": candle["t"],  # Keep the original timestamp
            "T": candle["T"],
            "s": candle["s"],
            "i": candle["i"],
            "haOpen": round(haOpen, 6),
            "haClose": round(haClose, 6),
            "haHigh": round(haHigh, 6),
            "haLow": round(haLow, 6),
            "v": candle["v"],  # Volume remains unchanged
            "n": candle["n"]
        }
        heikinAshiCandles.append(haCandle)
    return heikinAshiCandles
