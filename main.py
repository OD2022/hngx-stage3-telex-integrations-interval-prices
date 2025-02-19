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
                "app_description": "A brief description of the application functionality.",
                "app_logo": "URL to the application logo.",
                "app_name": "Name of the application.",
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
                    "display_name": "Performance Monitor"
                }
            },
            "settings": [
                {
                    "label": "interval",
                    "type": "text",
                    "required": True,
                    "default": "* * * * *"
                },
                {
                    "label": "Key",
                    "type": "text",
                    "required": True,
                    "default": "1234567890"
                },
                {
                    "label": "Do you want to continue",
                    "type": "checkbox",
                    "required": True,
                    "default": "Yes"
                },
                {
                    "label": "Provide Speed",
                    "type": "number",
                    "required": True,
                    "default": "1000"
                },
                {
                    "label": "Sensitivity Level",
                    "type": "dropdown",
                    "required": True,
                    "default": "Low",
                    "options": ["High", "Low"]
                },
                {
                    "label": "Alert Admin",
                    "type": "multi-checkbox",
                    "required": True,
                    "default": "Super-Admin",
                    "options": ["Super-Admin", "Admin", "Manager", "Developer"]
                }
            ],
            "tick_url": str(request.base_url) + "/tick"
        }
    }




@app.post("/tick", status_code=202)
def monitor(payload: MonitorPayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(monitor_task, payload)
    return {"status": "accepted"}