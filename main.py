from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.get("/api/hello")
async def hello(request: Request, visitor_name: str):

    if visitor_name is None:
        return {"error": "Visitor name is required."}

    # Strip surrounding single or double quotes if present
    if visitor_name.startswith(("'", '"')) and visitor_name.endswith(("'", '"')):
        visitor_name = visitor_name[1:-1]

    # Get the client IP from X-Forwarded-For header or fallback to request.client.host
    client_ip = request.headers.get('X-Forwarded-For', request.client.host).split(',')[0].strip()
    

    # Default location to "Location unavailable"
    location = "Location unavailable"
    
    try:
        # Make an asynchronous request to the IP geolocation API
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://ip-api.com/json/{client_ip}")
            response.raise_for_status()  # Raises an HTTPStatusError if the status code is 4xx or 5xx
            location_data = response.json()


            # Ensure location_data is a dictionary
            if isinstance(location_data, dict):
                location = location_data.get("city", "Location unavailable")
    except httpx.RequestError as e:
        # Handle general network errors
        print(f"Error fetching location data: {e}")
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {e}")


    greeting = "Hello, {}!".format(visitor_name.capitalize())


    # Return the response directly as a Python dictionary
    return {
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    }
