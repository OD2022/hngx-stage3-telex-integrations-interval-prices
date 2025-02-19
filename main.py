from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks
from MonitorPayload import *

app = FastAPI()

@app.get("/integration.json")
def get_integration_json(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return {
        "data": {
            "descriptions": {
                "app_name": "Uptime Monitor",
                "app_description": "Monitors website uptime",
                "app_url": base_url,
                "app_logo": "https://i.imgur.com/lZqvffp.png",
                "background_color": "#fff"
            },
            "integration_type": "interval",
            "settings": [
                {"label": "site-1", "type": "text", "required": True, "default": ""},
                {"label": "site-2", "type": "text", "required": True, "default": ""},
                {"label": "interval", "type": "text", "required": True, "default": "* * * * *"}
            ],
            "tick_url": f"{base_url}/tick",
            "key_features": [
                "Monitor multiple websites",
                "Customizable uptime checks",
                "Easy-to-use interface",
                "Cron-based interval scheduling"
            ],
            "integration_category": "Finance & Payments"  
        }
    }



@app.post("/tick", status_code=202)
def monitor(payload: MonitorPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(monitor_task, payload)
    return {"status": "accepted"}