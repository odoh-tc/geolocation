from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

@app.get("/api/hello")
async def hello(request: Request, visitor_name: str):

    if visitor_name is None:
        return {"error": "Visitor name is required."}

    if visitor_name.startswith(("'", '"')) and visitor_name.endswith(("'", '"')):
        visitor_name = visitor_name[1:-1]

    client_ip = request.headers.get('X-Forwarded-For', request.client.host).split(',')[0].strip()
    
    location = "Location unavailable"
    temperature = "Unavailable"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://ip-api.com/json/{client_ip}")
            response.raise_for_status() 
            location_data = response.json()

            if isinstance(location_data, dict):
                location = location_data.get("city", "Location unavailable")
                if location != "Location unavailable":
                    weather_response = await client.get(
                        f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={OPENWEATHERMAP_API_KEY}"
                    )
                    weather_response.raise_for_status()
                    weather_data = weather_response.json()

                    if isinstance(weather_data, dict):
                        main_data = weather_data.get("main", {})
                        temperature = main_data.get("temp", "Unavailable")
    except httpx.RequestError as e:
        print(f"Error fetching data: {e}")
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    greeting = f"Hello, {visitor_name.capitalize()}!, the temperature is {temperature} degrees Celsius in {location}"

    return {
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    }
