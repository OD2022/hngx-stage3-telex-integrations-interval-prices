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
    return {
        "data": {
            "date": {
                "created_at": "2025-02-19",  # Date of creation
                "updated_at": current_date   # Date of last update
            },
            "descriptions": {
                "app_description": "Get the prices of precious metals around the world.",
                "app_logo": "https://img.freepik.com/free-psd/shiny-gold-silver-bars-precious-metals-wealth-luxury-finance_632498-58760.jpg?t=st=174",
                "app_name": "Oluwakiitz Precious Metals Monitor",
                "app_url": str(request.base_url),
                "background_color": "#5F9EA0"
            },
            "integration_category": "Finance & Payments",
            "author": "Ibukun-Oluwa Addy",
            "integration_type": "interval",
            "is_active": False,
            "website": str(request.base_url),
            "output": [
                {"label": "output_channel_1", "value": True},
                {"label": "output_channel_2", "value": False}
            ],
            "key_features": [
                "-Monitors Metal Prices Around the world every 10 minutes"
            ],
            
            "settings": [
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "*/10 * * * *"
                }
                ,
                {
                    "label": "Stock Symbol",
                    "type": "text",
                    "required": True,
                    "default": "AAPL"
                }
            ],
            "tick_url": str(request.base_url) + "tick",
            "target_url": ""
                            }
    }




@app.post("/tick", status_code=202)
def monitor(payload: MonitorPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(monitor_task, payload)
    return {"status": "accepted"}