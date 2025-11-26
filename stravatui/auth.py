import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from stravalib.client import Client


def _refresh_access_token(refresh_token: str) -> dict:
    """Check and refresh access_token if it's expired."""
    load_dotenv()

    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": os.getenv("STRAVA_CLIENT_ID"),
            "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
    )

    if response.status_code != 200:
        raise Exception(
            f"Token refresh failed: {response.status_code} {response.text}\n"
            "Please re-run the authorisation script."
        )

    return response.json()


def _initialise_strava_client() -> Client:
    """Initialise a Strava client with the user's access token."""
    token_file = Path("strava_token.json")

    if not token_file.exists():
        raise FileNotFoundError(
            "No token file found. Please run the authorisation script."
        )

    with open(token_file, "r") as f:
        user_data = json.load(f)

    current_time = time.time()
    expires_at = user_data.get("expires_at", 0)

    if current_time > (expires_at - 60):
        user_data = _refresh_access_token(user_data["refresh_token"])

        with open(token_file, "w") as f:
            json.dump(user_data, f, indent=2)

    client = Client()
    client.access_token = user_data.get("access_token")

    return client
