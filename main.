from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.get("/")
def home():
    return {"message": "API aktif"}

@app.post("/render")
async def render(request: Request):

    data = await request.json()

    mode = data.get("mode")
    style = data.get("style")
    roomType = data.get("roomType")
    size = data.get("size")
    roomImage = data.get("roomImage")
    products = data.get("products")

    prompt = f"""
    Photorealistic {style} {roomType} interior design.
    Room size is {size} square meters.
    Include these real furniture products: {products}.
    Ultra realistic office atmosphere.
    Architectural visualization.
    Luxury lighting.
    """

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1536x1024"
    }

    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=body
    )

    return response.json()
