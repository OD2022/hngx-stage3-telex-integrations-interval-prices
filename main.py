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
                "app_description": "Get the global prices of precious metals in USD.",
                "app_logo": "https://img.freepik.com/free-vector/realistic-gold-metallic-button-brushed-surface-texture_1017-17738.jpg?t=st=1740137405~exp=1740141005~hmac=c93ecdb97a52b51bb5ea27b470f81427c9bca3a658d59f0d8181ed75dd71e6aa&w=826",
                "app_name": "Oluwakiitz Precious Metals Monitor",
                "app_url": base_url,
                "background_color": "#FFD700"
            },
            "integration_category": "Finance & Payments",
            "author": "Ibukun-Oluwa Addy",
            "integration_type": "interval",
            "is_active": False,
            "website": base_url,
           
            "key_features": [
                "-Monitors Metal Prices Around the world every two hours"
            ],
                "settings": [
            {
                "label": "interval",
                "type": "text",
                "required": True,
                "default": "0 */5 * * *"
            },
           {
            "label": "Metal",
            "type": "dropdown",
            "required": True,
            "default": "gold",
            "options": ["gold", "silver", "platinum", "palladium", "copper", "aluminum", "lead", "nickel", "zinc"]
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