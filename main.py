from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from MonitorPayload import *
from datetime import datetime
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://staging.telextest.im", "http://telextest.im", "https://staging.telex.im", "https://telex.im"], # NB: telextest is a local url
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)


@app.get("/")
def get_home_page():
    return {"message": "Hello World"}


@app.get("/integration.json")
def get_integration_json(request: Request):
    current_date = datetime.now().strftime("%Y-%m-%d")  # Current date in YYYY-MM-DD format
    base_url = str(request.base_url).rstrip("/")
    return {
        "data": {
            "date": {
                "created_at": "2025-02-19",  # Date of creation
                "updated_at": "2025-02-20"   # Date of last update
            },
            "descriptions": {
                "app_description": "Get the prices of precious metals around the world.",
                "app_logo": "https://img.freepik.com/free-photo/closeup-shot-pile-shiny-gold-coins-bars_181624-60854.jpg?t=st=1740074311~exp=1740077911~hmac=7457c9ddb11c2c5796a5034d3531456adc8b8cca3eae39a66d4e725da2c98fd7&w=996",
                "app_name": "Oluwakiitz Precious Metals Monitor",
                "app_url": base_url,
                "background_color": "#5F9EA0"
            },
            "integration_category": "Finance & Payments",
            "author": "Ibukun-Oluwa Addy",
            "integration_type": "interval",
            "is_active": False,
            "website": base_url,
           
            "key_features": [
                "-Monitors Metal Prices Around the world every 10 minutes"
            ],
            "settings": [
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "*/30 * * * *"
                }
                ,
                {
                    "label": "Stock Symbol",
                    "type": "text",
                    "required": True,
                    "default": "AAPL"
                }
            ],
            "tick_url": f"{base_url}/tick",
            "target_url": ""
                            }
    }




@app.post("/tick", status_code=202)
def monitor(payload: MonitorPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(monitor_task, payload)
    return {"status": "success"}