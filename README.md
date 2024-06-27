# Geolocation Service

## Overview

This FastAPI application provides an endpoint to greet a user and determine their geolocation based on their IP address. It uses the `httpx` library to make asynchronous HTTP requests to an external IP geolocation API.

## Features

- **IP Geolocation**: Retrieves the city location based on the client's IP address.
- **Asynchronous Requests**: Uses `httpx.AsyncClient` for non-blocking HTTP requests.
- **Error Handling**: Robust error handling for network and HTTP errors.

## Requirements

- Python 3.7+
- FastAPI
- httpx
