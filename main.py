from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

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
    return {"message": "Mock API aktif"}

@app.post("/render")
async def render(request: Request):

    data = await request.json()

    mode = data.get("mode")
    style = data.get("style")
    roomType = data.get("roomType")
    size = data.get("size")
    products = data.get("products")

    # MOCK IMAGE (sabit bir görsel URL)
    fake_image_url = "https://images.unsplash.com/photo-1524758631624-e2822e304c36"

    return {
        "status": "success",
        "mode": mode,
        "message": "MOCK render üretildi",
        "image_url": fake_image_url,
        "input": {
            "style": style,
            "roomType": roomType,
            "size": size,
            "products": products
        }
    }
