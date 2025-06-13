from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get("/questions")
def get_stackoverflow_questions(tag: str = None, pagesize: int = 5):
    params = {
        "order": "desc",
        "sort": "creation",
        "site": "stackoverflow",
        "pagesize": pagesize
    }

    if tag:
        params["tagged"] = tag

    try:
        response = requests.get("https://api.stackexchange.com/2.3/questions", params=params)
        response.raise_for_status()
        data = response.json()
        questions = [
            {
                "title": item["title"],
                "score": item["score"],
                "tags": item["tags"],
                "link": item["link"]
            }
            for item in data.get("items", [])
        ]
        return {"questions": questions}
    except requests.RequestException as e:
        return {"error": str(e)}
