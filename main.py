from fastapi import FastAPI, Request, HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

WEATHERSTACK_API_KEY = os.getenv('WEATHERSTACK_API_KEY')

@app.get("/api/hello")
async def hello(request: Request, visitor_name: str):
    if not visitor_name:
        raise HTTPException(status_code=400, detail="Visitor name is required.")

    if visitor_name.startswith(("'", '"')) and visitor_name.endswith(("'", '"')):
        visitor_name = visitor_name[1:-1]

    client_ip = request.headers.get('X-Forwarded-For', request.client.host).split(',')[0].strip()
    
    location = "Location unavailable"
    temperature = "Unavailable"

 
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://api.weatherstack.com/current",
            params={"access_key": WEATHERSTACK_API_KEY, "query": client_ip}
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            location = data.get("location", {}).get("name", "Location unavailable")
            temperature = data.get("current", {}).get("temperature", "Unavailable")


    greeting = f"Hello, {visitor_name.capitalize()}! The temperature is {temperature} degrees Celsius in {location}"

    return {
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    }
