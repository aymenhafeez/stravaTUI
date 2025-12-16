import json
import os
import urllib.parse
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from loguru import logger

PACKAGE_DIR = Path(__file__).parent
token_file = PACKAGE_DIR / "strava_token.json"

load_dotenv()

app = FastAPI(title="Strava OAuth", version="2.0")


def authorize_url():
    client_id = os.getenv("STRAVA_CLIENT_ID")
    if not client_id:
        raise HTTPException(500, "STRAVA_CLIENT_ID not set")
    app_url = os.getenv("APP_URL", "http://localhost")
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": f"{app_url}:5042/authorization_successful",
        "scope": "read,profile:read_all,activity:read_all",
        "state": "https://github.com/aymenhafeez/strava-oauth",
        "approval_prompt": "force",
    }
    return "https://www.strava.com/oauth/authorize?" + urllib.parse.urlencode(params)


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h1>Strava OAuth</h1>
    <p><a href="/authorize">Login with Strava</a></p>
    <p><a href="/my_activities">View My Activities</a></p>
    """


@app.get("/authorize")
async def authorize():
    return RedirectResponse(authorize_url())


@app.get("/authorization_successful")
async def exchange_token(code: Optional[str] = None):
    if not code:
        raise HTTPException(400, "No code")

    r = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": os.getenv("STRAVA_CLIENT_ID"),
            "client_secret": os.getenv("STRAVA_CLIENT_SECRET"),
            "code": code,
            "grant_type": "authorization_code",
        },
    )
    logger.debug(f"Strava token response: {r.status_code} {r.text}")
    data = r.json()

    # Save token
    with open(token_file, "w") as f:
        json.dump(data, f, indent=2)

    return HTMLResponse(f"""
    <h2>Success!</h2>
    <pre>{json.dumps(data, indent=2)}</pre>
    <p>Token saved to <code>strava_token.json</code></p>
    <a href="/">Back</a>
    """)


@app.get("/my_activities")
async def my_activities():
    try:
        with open(token_file) as f:
            token = json.load(f)["access_token"]
    except:
        return HTMLResponse("No token. <a href='/authorize'>Login first</a>")

    r = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers={"Authorization": f"Bearer {token}"},
        params={"per_page": 5},
    )
    activities = r.json()
    return HTMLResponse(f"""
    <h2>Last 5 Activities</h2>
    <ul>
    {"".join(f"<li><strong>{a['name']}</strong> – {a['distance'] / 1000:.1f}km</li>" for a in activities)}
    </ul>
    <a href="/">Back</a>
    """)
