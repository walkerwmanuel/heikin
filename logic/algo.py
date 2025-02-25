def buyWithTrend(heikinCandles, regularCandles):
    inTrade = False
    totalCash = 1000
    coinsOwned = 0

    for i, heikinCandle in enumerate(heikinCandles):
        openPrice = float(heikinCandle["haOpen"])
        closePrice = float(heikinCandle["haClose"])
        regularClosePrice = float(regularCandles[i]["c"])

        # Signal to buy
        if not inTrade and closePrice > openPrice:
            coinsOwned = totalCash / regularClosePrice
            inTrade = True
            continue

        # Signal to sell
        if inTrade and closePrice < openPrice:
            totalCash = coinsOwned * regularClosePrice
            inTrade = False
            continue

        # Close position at current time
        if i == len(heikinCandles) - 1 and inTrade:
            totalCash = coinsOwned * regularClosePrice

    return totalCash
