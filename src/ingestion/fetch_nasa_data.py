import requests
import sys
from datetime import datetime

import os
from dotenv import load_dotenv
load_dotenv()

def fetch_nasa_data(start_date, end_date):
    """
    Fetches Near Earth Object data from NASA's open API between given start and end dates.
    Returns the raw JSON data (as a Python dict).
    """
    # Step 1: Load credentials
    nasa_api_key = os.getenv("NASA_API_KEY")
    if not nasa_api_key:
        print("NASA_API_KEY not found in environment. Exiting.")
        sys.exit(1)

    # Step 2: Construct the request parameters
    api_endpoint = "https://api.nasa.gov/neo/rest/v1/feed"
    params = {
        "api_key": nasa_api_key,
        "start_date": start_date,
        "end_date": end_date
    }

    # Step 3: Make the HTTP GET request
    try:
        response = requests.get(api_endpoint, params=params)
        response.raise_for_status()  # Raise an error if the request failed
        data = response.json()
        return data
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":

    start_date = '2025-01-01'
    end_date = datetime.now().date().strftime("%Y-%m-%d")

    print(f"Fetching NASA data from {start_date} to {end_date}...")
    result = fetch_nasa_data(start_date, end_date)

    near_earth_objects = result.get("near_earth_objects", {})
    total_asteroids = sum(len(asteroids) for asteroids in near_earth_objects.values())
    print(f"Total asteroids fetched: {total_asteroids}")
