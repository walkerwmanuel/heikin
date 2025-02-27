from logic.volume import calculateVWAPOfCandles, calculateAvgVolOfCandles

def longAllHeikinGreen(heikinCandles, regularCandles, startingCash, leverage):
    inTrade = False

    for i, heikinCandle in enumerate(heikinCandles):
        heikinOpen = float(heikinCandle["haOpen"])
        heikinClose = float(heikinCandle["haClose"])
        regularClosePrice = float(regularCandles[i]["c"])

        # Signal to buy
        if not inTrade and heikinClose > heikinOpen:
            coinsOwned = (startingCash * leverage) / regularClosePrice
            inTrade = True
            continue

        # Signal to sell
        if inTrade and heikinOpen > heikinClose:
            startingCash = coinsOwned * regularClosePrice
            inTrade = False
            continue

        # Close position at current time
        if i == len(heikinCandles) - 1 and inTrade:
            startingCash = coinsOwned * regularClosePrice

    return startingCash

def shortAllHeikinRed(heikinCandles, regularCandles, startingCash, leverage):
    inTrade = False
    entryPrice = None
    positionSize = 0
    numofshorts = 0

    for i, heikinCandle in enumerate(heikinCandles):
        heikinOpen = float(heikinCandle["haOpen"])
        heikinClose = float(heikinCandle["haClose"])
        regularClosePrice = float(regularCandles[i]["c"])

        # Signal to short (enter position)
        if not inTrade and heikinOpen > heikinClose:
            entryPrice = regularClosePrice
            # Size of short position: margin * leverage
            positionSize = (startingCash * leverage) / entryPrice
            inTrade = True
            numofshorts += 1
            continue

        # Signal to cover short (exit position)
        if inTrade and heikinClose > heikinOpen:
            # PnL for a short: (entryPrice - exitPrice) * positionSize
            pnl = (entryPrice - regularClosePrice) * positionSize
            startingCash += pnl
            inTrade = False
            continue

        # Close position at current time if still in trade
        if i == len(heikinCandles) - 1 and inTrade:
            pnl = (entryPrice - regularClosePrice) * positionSize
            startingCash += pnl
            inTrade = False
    print(numofshorts)
    return startingCash

def shortInHighVol(heikinCandles, regularCandles, startingCash, leverage):
    inTrade = False
    entryPrice = None
    positionSize = 0
    numofshorts = 0

    for i, heikinCandle in enumerate(heikinCandles):

        if i > 288:
            heikinOpen = float(heikinCandle["haOpen"])
            heikinClose = float(heikinCandle["haClose"])
            regularClosePrice = float(regularCandles[i]["c"])

            avgVol24Hours = calculateAvgVolOfCandles(regularCandles[i-287:i+1])
            avgVol30Minutes = calculateAvgVolOfCandles(regularCandles[i-5:i+1])
            # print(avgVol24Hours)
            # print(avgVol30Minutes)
            if avgVol30Minutes > avgVol24Hours * 4 and not inTrade:
            # Signal to short (enter position)
                if heikinOpen > heikinClose:
                    entryPrice = regularClosePrice
                    # Size of short position: margin * leverage
                    positionSize = (startingCash * leverage) / entryPrice
                    inTrade = True
                    numofshorts += 1
                    print(i)
                    continue

            # Signal to cover short (exit position)
            if inTrade and heikinClose > heikinOpen:
                # PnL for a short: (entryPrice - exitPrice) * positionSize
                pnl = (entryPrice - regularClosePrice) * positionSize
                startingCash += pnl
                inTrade = False
                continue

            # Close position at current time if still in trade
            if i == len(heikinCandles) - 1 and inTrade:
                pnl = (entryPrice - regularClosePrice) * positionSize
                startingCash += pnl
                inTrade = False
    print(numofshorts)
    return startingCash