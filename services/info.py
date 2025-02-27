import websockets
import json
import time
import requests

async def getCandles(coin, interval):
    url = "wss://api.hyperliquid.xyz/ws"  # WebSocket API endpoint
    
    async with websockets.connect(url) as ws:
        # Subscribe to SUI 5-minute candlesticks
        subscribeMessage = {
            "method": "subscribe",
            "subscription": {
                "type": "candle",
                "coin": coin,
                "interval": interval
            }
        }

        await ws.send(json.dumps(subscribeMessage))  # Send the subscription request
        
        # Continuously receive and print incoming candle data
        while True:
            response = await ws.recv()
            candleData = json.loads(response)
            print("Received:", candleData)  # Print the live candle data

def getCandleSnapshot(coin, interval):
    url = "https://api.hyperliquid.xyz/info"  # Hyperliquid API endpoint

    headers = {
        "Content-Type": "application/json"
    }

    # Get current timestamp (in milliseconds)
    end_time = int(time.time() * 1000)
    
    # number of candles you want * minutes inside of candle * 60000 to convert ms to hours
    start_time = end_time - (2880 * 5 * 60000)

    # Request payload
    payload = {
        "type": "candleSnapshot",
        "req": {
            "coin": coin,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time
        }
    }

    # Send API request
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data
        
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
