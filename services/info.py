import websockets
import json
import time
import requests
import datetime

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

    # Create a datetime object for February 28, 2025 at 00:01:00 UTC
    target_date = datetime.datetime(2025, 2, 28, 0, 1, 0, tzinfo=datetime.timezone.utc)
    # Convert to Unix timestamp (seconds since epoch)
    timestamp_seconds = target_date.timestamp()
    # Convert to milliseconds
    end_time = int(timestamp_seconds * 1000)
    
    # number of minutes you want * 60000 - 14400 is 10 days in minutes
    start_time = end_time - (14400 * 60000)

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
