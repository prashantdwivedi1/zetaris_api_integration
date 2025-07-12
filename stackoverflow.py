from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime
import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get credentials from environment variables (or set directly here for testing)
STACK_CLIENT_ID = os.getenv("STACK_CLIENT_ID", "")
STACK_CLIENT_SECRET = os.getenv("STACK_CLIENT_SECRET", "")
# STACK_KEY = os.getenv("STACK_KEY", "")  # Optional if you want to include a key
STACK_API_URL = "https://api.stackexchange.com/2.3/search"

# Helper to convert date to UNIX timestamp
def to_unix(date_str: Optional[str]) -> Optional[int]:
    if not date_str:
        return None
    try:
        # Try ISO format (handles YYYY-MM-DD and YYYY-MM-DDTHH:MM:SS)
        return int(datetime.fromisoformat(date_str).timestamp())
    except ValueError:
        # Fallback: truncate to just YYYY-MM-DD if needed
        return int(datetime.strptime(date_str[:10], "%Y-%m-%d").timestamp())

@app.get("/search_stackoverflow")
async def search_stackoverflow(
    keyword: str,
    from_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD"),
    to_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD"),
    sort: Optional[str] = Query("relevance", description="Sort by 'activity', 'votes', 'creation', 'relevance'"),
    order: Optional[str] = Query("desc", description="Order by 'asc' or 'desc'"),
    site: Optional[str] = Query("stackoverflow", description="StackExchange site (default: stackoverflow)")
):
    params = {
        "intitle": keyword,
        "sort": sort,
        "order": order,
        "site": site,
        "client_id": STACK_CLIENT_ID,
        "client_secret": STACK_CLIENT_SECRET,
        # "key": STACK_KEY,  # Optional
    }

    from_ts = to_unix(from_date)
    to_ts = to_unix(to_date)

    if from_ts:
        params["fromdate"] = from_ts
    if to_ts:
        params["todate"] = to_ts

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(STACK_API_URL, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        return {"error": f"HTTP request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Something went wrong: {str(e)}"}
