from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks
from MonitorPayload import *
from datetime import datetime
app = FastAPI()


@app.get("/")
def get_home_page():
    return {"message": "Hello World"}


@app.get("/integration.json")
def get_integration_json(request: Request):
    current_date = datetime.now().strftime("%Y-%m-%d")  # Current date in YYYY-MM-DD format
    return {
        "data": {
            "date": {
                "created_at": current_date,  # Date of creation
                "updated_at": current_date   # Date of last update
            },
            "descriptions": {
                "app_description": "Get the prices of precious metals around the world.",
                "app_logo": "https://img.freepik.com/free-psd/shiny-gold-silver-bars-precious-metals-wealth-luxury-finance_632498-58760.jpg?t=st=174",
                "app_name": "Oluwakiitz Precious Metals Monitor",
                "app_url": str(request.base_url),
                "background_color": "#HEXCODE"
            },
            "integration_category": "Finance & Payments",
            "integration_type": "interval",
            "is_active": False,
            "output": [
                {"label": "output_channel_1", "value": True},
                {"label": "output_channel_2", "value": False}
            ],
            "key_features": [
                "Feature description 1.",
                "Feature description 2.",
                "Feature description 3.",
                "Feature description 4."
            ],
            "permissions": {
                "monitoring_user": {
                    "always_online": True,
                    "display_name": "Oluwakiitz Metals"
                }
            },
            "settings": [
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "* * * * *"
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
            "target_url": "https://ping.telex.im/v1/webhooks/01951a74-7505-7819-9350-db49b64c7941"
                            }
    }




@app.post("/tick", status_code=202)
def monitor(payload: MonitorPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(monitor_task, payload)
    return {"status": "accepted"}