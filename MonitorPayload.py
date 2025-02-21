import os
from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import List
import httpx
import asyncio

load_dotenv() 

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

# Fetch precious metals data using Alpha Vantage (for free tier)
async def fetch_precious_metals_data(metal: str) -> str:
    # Get the API key from environment variables (from Alpha Vantage)
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key not found in environment variables")

    # Alpha Vantage API endpoint for commodities (gold, silver)
    if metal.lower() == "gold":
        url = f"https://www.alphavantage.co/query?function=COMMODITY_MONTHLY&symbol=XAUUSD&apikey={api_key}"
    elif metal.lower() == "silver":
        url = f"https://www.alphavantage.co/query?function=COMMODITY_MONTHLY&symbol=XAGUSD&apikey={api_key}"
    else:
        raise HTTPException(status_code=400, detail="Unsupported metal. Only gold and silver are available.")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                if "Monthly Adjusted Commodity Prices" in data:
                    monthly_data = data["Monthly Adjusted Commodity Prices"]
                    latest_month = list(monthly_data.keys())[0]
                    price = monthly_data[latest_month]["close"]
                    return f"Current {metal.capitalize()} price (USD): ${price}"
                return "No monthly commodity price data found."
            return f"Alpha Vantage API error: {response.status_code}"
    except Exception as e:
        return f"Error fetching data: {str(e)}"



# Background task for monitoring
async def monitor_task(payload: MonitorPayload):
    # Extract Metal from settings
    metal = next((s.default for s in payload.settings if s.label == "Metal"), None)
    
    if not metal:
        raise HTTPException(status_code=400, detail="Metal missing from settings")
    
    # Fetch precious metals data
    metal_data = await fetch_precious_metals_data(metal)

    # Prepare the data to send back to the return_url
    data = {
        "message": metal_data,
        "username": "Precious Metal Price Checker",
        "event_name": f"{metal.capitalize()} Price Check",
        "status": "success" 
    }

    headers = {"Content-Type": "application/json"}
    # Send the response to the return_url
    async with httpx.AsyncClient() as client:
        await client.post(payload.return_url, json=data, headers=headers)

