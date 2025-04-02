from logic.volume import calculateVWAPOfCandles, calculateAvgVolOfCandles

def longAllHeikinGreen(heikinCandles, regularCandles, currCash, leverage):
    inTrade = False

    for i, heikinCandle in enumerate(heikinCandles):
        heikinOpen = float(heikinCandle["haOpen"])
        heikinClose = float(heikinCandle["haClose"])
        regularClosePrice = float(regularCandles[i]["c"])
        heikinCloseTime = float(heikinCandle["T"])
        # Signal to buy
        if not inTrade and heikinClose > heikinOpen and i > 0:
            coinsOwned = (currCash * leverage) / regularClosePrice
            inTrade = True
            print(f"enter long at candle ", i, "TimeStamp", heikinCloseTime)
            continue

        # Signal to sell
        if inTrade and heikinOpen > heikinClose:
            currCash = (coinsOwned * regularClosePrice) * .9998
            inTrade = False
            print(f"exit long at candle ", i, "now our cash is ", currCash, " TimeStamp ", heikinCloseTime)
            continue

        # Close position at current time
        if i == len(heikinCandles) - 1 and inTrade:
            currCash = coinsOwned * regularClosePrice
            print(f"exit long at candle ", i, "now our cash is ", currCash, " TimeStamp ", heikinCloseTime)

    return currCash

def shortAllHeikinRed(heikinCandles, regularCandles, startingCash, leverage):
    inTrade = False
    entryPrice = None
    positionSize = 0
    numofshorts = 0

    for i, heikinCandle in enumerate(heikinCandles):
        heikinOpen = float(heikinCandle["haOpen"])
        heikinClose = float(heikinCandle["haClose"])
        regularClosePrice = float(regularCandles[i]["c"])
        heikinCloseTime = float(heikinCandle["T"])


        # Signal to short (enter position)
        if not inTrade and heikinOpen > heikinClose:
            entryPrice = regularClosePrice
            # Size of short position: margin * leverage
            positionSize = (startingCash * leverage) / entryPrice
            inTrade = True
            numofshorts += 1
            print(f"enter short at candle ", i, "at a market price of", regularClosePrice, " TimeStamp ", heikinCloseTime)
            continue

        # Signal to cover short (exit position)
        if inTrade and heikinClose > heikinOpen:
            # PnL for a short: (entryPrice - exitPrice) * positionSize
            pnl = (entryPrice - regularClosePrice) * positionSize
            startingCash += pnl
            print(f"exit short at candle ", i, "the exit price is", regularClosePrice, "and the pnl is ", pnl, " TimeStamp ", heikinCloseTime)
            inTrade = False
            continue

        # Close position at current time if still in trade
        if i == len(heikinCandles) - 1 and inTrade:
            pnl = (entryPrice - regularClosePrice) * positionSize
            startingCash += pnl
            inTrade = False
            print(f"exit short at candle ", i, "the exit price is", regularClosePrice, "and the pnl is ", pnl, " TimeStamp ", heikinCloseTime)
    return startingCash

def isInTrade(s, l):
    return s or l

def shortAndLongAllHeikin(heikinCandles, regularCandles, startingCash, leverage):
    inShortTrade = False
    inLongTrade = False
    entryPrice = None
    positionSize = 0
    numofshorts = 0

    for i, heikinCandle in enumerate(heikinCandles):
        heikinOpen = float(heikinCandle["haOpen"])
        heikinClose = float(heikinCandle["haClose"])
        regularClosePrice = float(regularCandles[i]["c"])
        # Signal to short (enter position)
        if not isInTrade(inShortTrade, inLongTrade) and heikinOpen > heikinClose:
            entryPrice = regularClosePrice
            # Size of short position: margin * leverage
            positionSize = (startingCash * leverage) / entryPrice
            inShortTrade = True
            numofshorts += 1
            print(f"enter short at candle ", i, "at a market price of", regularClosePrice)
            continue
        if not isInTrade(inShortTrade, inLongTrade) and heikinOpen > heikinClose:
            entryPrice = regularClosePrice
            # Size of short position: margin * leverage
            positionSize = (startingCash * leverage) / entryPrice
            inLongTrade = True
            numofshorts += 1
            print(f"enter short at candle ", i, "at a market price of", regularClosePrice)
            continue

        # Signal to cover short (exit position)
        if inShortTrade and heikinClose > heikinOpen:
            # PnL for a short: (entryPrice - exitPrice) * positionSize
            pnl = (entryPrice - regularClosePrice) * positionSize
            startingCash += pnl
            print(f"exit short at candle ", i, "the exit price is", regularClosePrice, "and the pnl is ", pnl)
            inShortTrade = False
                        # PnL for a short: (entryPrice - exitPrice) * positionSize
            entryPrice = regularClosePrice
            # Size of short position: margin * leverage
            positionSize = (startingCash * leverage) / entryPrice
            inLongTrade = True
            numofshorts += 1
            print(f"enter long at candle ", i, "at a market price of", regularClosePrice)
            continue
        if inLongTrade and heikinClose > heikinOpen:
            # PnL for a short: (entryPrice - exitPrice) * positionSize
            pnl = (entryPrice - regularClosePrice) * positionSize
            startingCash += pnl
            print(f"exit long at candle ", i, "the exit price is", regularClosePrice, "and the pnl is ", pnl)
            inLongTrade = False
            entryPrice = regularClosePrice
            # Size of short position: margin * leverage
            positionSize = (startingCash * leverage) / entryPrice
            inShortTrade = True
            numofshorts += 1
            print(f"enter short at candle ", i, "at a market price of", regularClosePrice)
            continue

        # Close position at current time if still in trade
        if i == len(heikinCandles) - 1 and isInTrade(inShortTrade, inLongTrade):
            if inShortTrade:
                pnl = (entryPrice - regularClosePrice) * positionSize
                startingCash += pnl
                print(f"exit short at candle ", i, "the exit price is", regularClosePrice, "and the pnl is ", pnl)
            else:
                pnl = (entryPrice - regularClosePrice) * positionSize
                startingCash += pnl
                print(f"exit long at candle ", i, "the exit price is", regularClosePrice, "and the pnl is ", pnl)

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
            if avgVol30Minutes > avgVol24Hours * 3 and not inTrade:
            # Signal to short (enter position)
                if heikinOpen > heikinClose:
                    entryPrice = regularClosePrice
                    # Size of short position: margin * leverage
                    positionSize = (startingCash * leverage) / entryPrice
                    inTrade = True
                    numofshorts += 1
                    print(f"entered short at candle", i)
                    continue

            # Signal to cover short (exit position)
            if inTrade and heikinClose > heikinOpen:
                # PnL for a short: (entryPrice - exitPrice) * positionSize
                pnl = (entryPrice - regularClosePrice) * positionSize
                startingCash += pnl
                inTrade = False
                print(f"exit short at candle ", i, "the pnl is ", pnl)
                continue

            # Close position at current time if still in trade
            if i == len(heikinCandles) - 1 and inTrade:
                pnl = (entryPrice - regularClosePrice) * positionSize
                startingCash += pnl
                inTrade = False

    print(numofshorts)
    return startingCash

def fifteenAndTwelve(fifteenMHA, fifteenMC, twelveHHA, startingCash, leverage):

    # The point of this algorithm is to look for a green or red 12 hour heikin ashi candle and if it is green 
    # then the next 12 hours you will look for longs

    for i, heikinCandle in enumerate(twelveHHA):

        twelveHAOpen = float(heikinCandle["haOpen"])
        twelveHAClose = float(heikinCandle["haClose"])
        twelveHACloseTime = float(heikinCandle["T"])

        print(f"Look at me", twelveHAOpen, twelveHAClose, twelveHACloseTime)

        if twelveHAClose > twelveHAOpen and i > 0:
                # Look for longs
                # startingCash = longAllHeikinGreen(fifteenMHA[(i*48)+48:(i*48)+96], fifteenMC[(i*48)+48:(i*48)+96], startingCash, leverage)
                startingCash = longAllHeikinGreenWithThreshold(fifteenMHA[(i*48)+48:(i*48)+96], fifteenMC[(i*48)+48:(i*48)+96], startingCash, leverage, .02)


                continue
        if twelveHAClose < twelveHAOpen and i > 0:
                # Look for shorts
                # startingCash = shortAllHeikinRed(fifteenMHA[(i*48)+48:(i*48)+96], fifteenMC[(i*48)+48:(i*48)+96], startingCash, leverage)
                startingCash = shortAllHeikinRedWithThreshold(fifteenMHA[(i*48)+48:(i*48)+96], fifteenMC[(i*48)+48:(i*48)+96], startingCash, leverage, .02)

                continue
    print(f"The total amount of capital after trading is ", startingCash)
    return startingCash
    
        
def longAllHeikinGreenWithThreshold(heikinCandles, regularCandles, currCash, leverage, threshold=0.03):
    inTrade = False
    
    for i, heikinCandle in enumerate(heikinCandles):
        heikinOpen = float(heikinCandle["haOpen"])
        heikinClose = float(heikinCandle["haClose"])
        regularClosePrice = float(regularCandles[i]["c"])
        heikinCloseTime = float(heikinCandle["T"])
        
        # Signal to buy - check if candle is green AND close is > threshold% above open
        percentage_change = (heikinClose - heikinOpen) / heikinOpen
        
        if not inTrade and heikinClose > heikinOpen and percentage_change > threshold:
            coinsOwned = (currCash * leverage) / regularClosePrice
            inTrade = True
            print(f"enter long at candle {i}, %change: {percentage_change*100:.2f}%, TimeStamp: {heikinCloseTime}")
            continue

        # Signal to sell
        if inTrade and heikinOpen > heikinClose:
            currCash = (coinsOwned * regularClosePrice) * .9998
            inTrade = False
            print(f"exit long at candle {i}, now our cash is {currCash}, TimeStamp: {heikinCloseTime}")
            continue

        # Close position at current time
        if i == len(heikinCandles) - 1 and inTrade:
            currCash = coinsOwned * regularClosePrice
            print(f"exit long at candle {i}, now our cash is {currCash}, TimeStamp: {heikinCloseTime}")

    return currCash

def shortAllHeikinRedWithThreshold(heikinCandles, regularCandles, startingCash, leverage, threshold=0.03):
    inTrade = False
    entryPrice = None
    positionSize = 0
    
    for i, heikinCandle in enumerate(heikinCandles):
        heikinOpen = float(heikinCandle["haOpen"])
        heikinClose = float(heikinCandle["haClose"])
        regularClosePrice = float(regularCandles[i]["c"])
        heikinCloseTime = float(heikinCandle["T"])
        
        # Calculate percentage change for red candle
        percentage_change = (heikinOpen - heikinClose) / heikinOpen
        
        # Signal to short (enter position) - must be red AND exceed threshold
        if not inTrade and heikinOpen > heikinClose and percentage_change > threshold:
            entryPrice = regularClosePrice
            positionSize = (startingCash * leverage) / entryPrice
            inTrade = True
            print(f"enter short at candle {i}, %change: {percentage_change*100:.2f}%, price: {regularClosePrice}, TimeStamp: {heikinCloseTime}")
            continue

        # Signal to cover short (exit position)
        if inTrade and heikinClose > heikinOpen:
            pnl = (entryPrice - regularClosePrice) * positionSize
            startingCash += pnl
            print(f"exit short at candle {i}, exit price: {regularClosePrice}, pnl: {pnl}, TimeStamp: {heikinCloseTime}")
            inTrade = False
            continue

        # Close position at end of period if still in trade
        if i == len(heikinCandles) - 1 and inTrade:
            pnl = (entryPrice - regularClosePrice) * positionSize
            startingCash += pnl
            inTrade = False
            print(f"exit short at candle {i}, exit price: {regularClosePrice}, pnl: {pnl}, TimeStamp: {heikinCloseTime}")
    
    return startingCash