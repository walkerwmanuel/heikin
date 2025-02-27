def calculateAvgVolOfCandles(candlesData):
    sumVolume = 0
    
    for candle in candlesData:
        volume = float(candle["v"])
        sumVolume += volume

    # Compute the average once after summing
    volAvg = sumVolume / len(candlesData) if candlesData else 0
    if volAvg == 0:  # Safety check
        return None  
    
    return volAvg

def calculateVWAPOfCandles(candlesData):
    sumVwapOfCandles = 0
    sumVolume = 0
    
    for candle in candlesData:
        openPrice = float(candle["o"])
        highPrice = float(candle["h"])
        lowPrice = float(candle["l"])
        closePrice = float(candle["c"])
        volume = float(candle["v"])
        numOfTrades = float(candle["n"])
        # Calculate the "typical" price for this candle
        avgPrice = (highPrice + lowPrice + closePrice) / 3 
        vwapOfCandle = avgPrice * volume
        
        # Add to our running totals
        sumVwapOfCandles += vwapOfCandle
        sumVolume += volume

    if sumVolume == 0: # Safety check
        return None  
    
    return sumVwapOfCandles / sumVolume