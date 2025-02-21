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


async def fetch_precious_metals_data(metal: str) -> str:
    api_key = os.getenv("METALS_DEV_API_KEY")
    
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key not found in environment variables")

    # metals.dev API endpoint for metals (gold, silver, copper, etc.)
    metal_symbol = ""
    if metal.lower() == "gold":
        metal_symbol = "gold"
    elif metal.lower() == "silver":
        metal_symbol = "silver"
    elif metal.lower() == "platinum":
        metal_symbol = "platinum"
    elif metal.lower() == "palladium":
        metal_symbol = "palladium"
    elif metal.lower() == "copper":
        metal_symbol = "copper"
    elif metal.lower() == "aluminum":
        metal_symbol = "aluminum"
    elif metal.lower() == "lead":
        metal_symbol = "lead"
    elif metal.lower() == "nickel":
        metal_symbol = "nickel"
    elif metal.lower() == "zinc":
        metal_symbol = "zinc"
    else:
        raise HTTPException(status_code=400, detail="Unsupported metal. Available metals are gold, silver, platinum, palladium, copper, aluminum, lead, nickel, and zinc.")
    
    # Constructing the API URL with the provided format
    url = f"https://api.metals.dev/v1/latest?api_key={api_key}&currency=USD&unit=toz&symbols={metal_symbol}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                if "status" in data and data["status"] == "success" and "metals" in data:
                    if metal_symbol in data["metals"]:
                        price = data["metals"][metal_symbol]
                        return f"Current {metal.capitalize()} price (USD per ounce): ${price}"
                    return f"Price data for {metal} is not available."
                return "Error: Unable to retrieve data from the Metals API."
            return f"Metals API error: {response.status_code}"
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

