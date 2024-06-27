from fastapi import FastAPI, Request
import httpx

app = FastAPI()

@app.get("/api/hello")
async def hello(request: Request, visitor_name: str):

    # Get the client IP from X-Forwarded-For header or fallback to request.client.host
    client_ip = request.headers.get('X-Forwarded-For', request.client.host).split(',')[0].strip()
    
    print(f"Client IP: {client_ip}")  # Log the client IP for debugging

    # Default location to the entire response if city is not available
    location = "Location unavailable"
    
    try:
        # Make an asynchronous request to the IP geolocation API
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://ip-api.com/json/{client_ip}")
            response.raise_for_status()  # Raises an HTTPStatusError if the status code is 4xx or 5xx
            location_data = response.json()
            print("Location data:", location_data)  # Log the response data for debugging
            
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

    # Construct the greeting message
    greeting = f"Hello, {visitor_name.capitalize()}!"

    # Return the response
    return {
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    }
