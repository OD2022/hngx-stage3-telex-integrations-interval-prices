import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import httpx
import asyncio

# Initialize FastAPI app
app = FastAPI()

# Define settings structure
class Setting(BaseModel):
    label: str
    type: str
    required: bool
    default: str

class MonitorPayload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]

# Fetch stock data from Alpha Vantage API
async def fetch_stock_data(symbol: str) -> str:
    # Get the API key from environment variables
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key not found in environment variables")

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={api_key}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                # Assuming we're just returning the latest close price from the time series data
                if "Time Series (5min)" in data:
                    latest_time = list(data["Time Series (5min)"].keys())[0]
                    latest_data = data["Time Series (5min)"][latest_time]
                    close_price = latest_data["4. close"]
                    return f"Stock {symbol} latest close price: {close_price}"
                return "No time series data found."
            return f"Alpha Vantage API error: {response.status_code}"
    except Exception as e:
        return f"Error fetching data: {str(e)}"

# Background task for monitoring
async def monitor_task(payload: MonitorPayload):
    # # Extract Stock Symbol from settings
    # symbol = next((s.default for s in payload.settings if s.label == "Stock Symbol"), None)
    
    # if not symbol:
    #     raise HTTPException(status_code=400, detail="Stock Symbol missing from settings")
    
    # # Fetch stock data from Alpha Vantage
    # stock_data = await fetch_stock_data(symbol)

    # Prepare the data to send back to the return_url
    data = {
        "message": "Hiiiiii",
        "username": "Financial Data Fetcher",
        "event_name": "Stock Price Check",
        "status": "success"
    }

    # Send the response to the return_url
    async with httpx.AsyncClient() as client:
        await client.post(payload.return_url, json=data)    

