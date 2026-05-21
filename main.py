from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import requests
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "V2 engine active"}

def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content)).convert("RGBA")

@app.post("/render")
async def render(request: Request):

    data = await request.json()

    mode = data.get("mode")
    room_image_url = data.get("roomImage")
    products = data.get("products")

    # MOCK: şimdilik sadece base image döndürüyoruz
    base_url = room_image_url or "https://images.unsplash.com/photo-1524758631624-e2822e304c36"

    return {
        "status": "v2_ready",
        "message": "Real staging engine base ready",
        "base_image": base_url,
        "products_received": products
    }
