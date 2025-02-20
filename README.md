# hngx-stage3-telex-integrations-interval-prices

## Introduction
The Precious Monitor monitors the prices of precious metals around the world.
This is an interval integration so you must define an interval in the settings for it to work. The default settings specify an interval field so when it is added to your organisation, you can go ahead to modify it. 

## Setting Up

This is a FastAPI project and has its dependencies defined in the requirements.txt. This means you can use pip or any other package manager to install depdencies. For an easier install, use uv by following the steps below:

1. **Install uv**: You can install it using pip or another package manager:
    ```bash
    pip install uv
    ```

2. **Sync dependencies**: Run the following command to synchronize dependencies (basically installs dependencies if you haven't before):
    ```bash
    uv sync
    ```

3. **Run the application**: Start the application with the command:
    ```bash
    uv run main.py
    ```
    
    You could also run in watch mode using:

   ```bash
   source .venv/bin/active # .venv/Scripts/activate for Windows
   uvicorn main:app --reload
   ```

The server should now be running and accessible at `http://localhost:8000`.

## Integration JSON

The integration JSON file defined at the route `/integration.json` defines all the details needed for this integration to work on Telex. Since it is an interval integration that doesn't need data, it only exposes a /tick_url endpoint. Telex will call this endpoint according to the cron interval defined in the settings. The JSON snippet below shows the uptime json for the deployed url at: https://telex-fastapi-uptime-monitor.onrender.com/integration.json. If you deploy it somewhere else, the `app_url`, `website`, and `tick_url` will be updated. 

```json
{
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
```

## Request Format

The `/tick` endpoint accepts a `POST` request with the following JSON payload:

```json
{
  "channel_id": "01951a74-7505-7819-9350-db49b64c7941",
  "return_url": "https://ping.telex.im/v1/webhooks/01951a74-7505-7819-9350-db49b64c7941",
  "settings": [
    {
      "label": "interval",
      "type": "text",
      "required": true,
      "default": "* * * * *"
    },
    
    {
      "label": "Stock Symbol",
      "type": "text",
      "required": true,
      "default": "AAPL"
    }
  ]
}

```

This data will be sent by Telex each time the cron interval is reached. The default interval is defined as `* * * * *` which means every minute according to cron-syntax. Use https://crontab.guru for help defining cron schedules. The integration reads the settings to figure out the sites that must be called immediately, then sends a response, if any, to the `return_url` provided by Telex. 

NB: The `channel_id` has no exact use in this particular integration but could be extremely useful for an integration that must distinguish between channels, like a summarizer that defines an interval of 6 pm every day, and must stores accumulated messages in its local storage (sqlite, postgres, txt file, whatever it may be), and summarize them (reach out to the devs for more ideas like this).

### Explanation:
- `channel_id`: The ID of the Telex channel.
- `return_url`: The URL where the monitoring results will be sent.
- `settings`: An array of settings for the monitored sites. The settings are defined by the integration author and can only be used by the author. Telex only sends the settings whenever the /tick_url is called.


### Response:
- **202 Accepted**: The monitoring task has been accepted and is running in the background.

## Background Handling

Monitoring tasks run asynchronously in the background. Telex has a low tolerance for delays and will time out after approximately one second. To accommodate this:

- Monitoring requests are accepted immediately with a `202` response.
- The actual site checks are performed asynchronously in a background task.
- Only sites that respond within the specified timeout are reported.

**Important:** Make sure your integration returns an accepted response to Telex, then proceed to do processing in the background, returning results to the channel when this processing is complete. This ensures it can receive many other requests and is kept fast.

## Contributing

Contributions are welcome! This project is licensed under the MIT License.

### Steps to Contribute:
1. Fork the repository.
2. Create a new branch with your feature or bugfix.
3. Submit a pull request for review.

### License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it under the terms of the license.

---

Happy monitoring! 😊

