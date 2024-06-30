# Geolocation Service

## Overview

This FastAPI application provides an endpoint to greet a user and determine their geolocation based on their IP address. It utilizes the `httpx` library to perform asynchronous HTTP requests to an external IP geolocation API. Additionally, it also includes functionality to retrieve the temperature of the location.

## Features

- **IP Geolocation**: Retrieves the city location based on the client's IP address.
- **Temperature Retrieval**: Provides the current temperature of the geolocated city.
- **Asynchronous Requests**: Uses `httpx.AsyncClient` for efficient and non-blocking HTTP requests.
- **Error Handling**: Implements robust error handling mechanisms for network and HTTP errors.

## Requirements

- Python 3.7+
- FastAPI
- httpx
