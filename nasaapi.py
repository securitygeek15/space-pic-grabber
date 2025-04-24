import requests
import random
import os
import time
from concurrent.futures import ThreadPoolExecutor

api_key = os.getenv("NASA_API_KEY")
os.makedirs("nasa_images", exist_ok=True)

def fetch_and_save(i):
    apod_url = "https://api.nasa.gov/planetary/apod"
    year = str(random.randint(1995, 2024))
    month = str(random.randint(1, 12)).zfill(2)
    day = str(random.randint(1, 28)).zfill(2)
    date = f"{year}-{month}-{day}"

    params = {"api_key": api_key, "date": date}

    try:
        response = requests.get(apod_url, params=params)
        if response.status_code == 200:
            data = response.json()
            image_url = data.get("hdurl") or data.get("url")
            if data.get("media_type") == "image" and image_url:
                img = requests.get(image_url)
                with open(f"nasa_images/{i}.jpg", "wb") as f:
                    f.write(img.content)
                print(f"{i}: {date}")
            else:
                print(f"{i}: Not image - {date}")
        elif response.status_code == 403:
            print(f"{i}: API error 403 - {date}")
        else:
            print(f"{i}: API error {response.status_code} - {date}")
    except Exception as e:
        print(f"{i}: Error - {e} - {date}")

    time.sleep(1)  # Small delay to avoid hitting rate limits

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(fetch_and_save, range(10))
