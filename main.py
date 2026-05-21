from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import requests
from io import BytesIO
import base64

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_image(url):
    try:
        if not url:
            return None
        r = requests.get(url, timeout=10)
        return Image.open(BytesIO(r.content)).convert("RGBA")
    except:
        return None

def resize(img, scale):
    w, h = img.size
    return img.resize((int(w * scale), int(h * scale)))

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/render")
async def render(request: Request):

    data = await request.json()

    room_url = data.get("roomImage")
    products = data.get("products", "")

    # fallback background
    base = load_image(room_url)

    if base is None:
        base = Image.new("RGBA", (1200, 800), (240, 240, 240))

    base_w, base_h = base.size

    product_list = []
    if products:
        product_list = [p.strip() for p in products.split(",") if p.strip()]

    x = 50
    y = int(base_h * 0.6)

    for i, url in enumerate(product_list):

        img = load_image(url)

        if img is None:
            continue

        scale = max(0.2 - (i * 0.03), 0.1)
        img = resize(img, scale)

        base.paste(img, (x, y), img)

        x += img.size[0] + 20

    buffer = BytesIO()
    base.save(buffer, format="PNG")

    encoded = base64.b64encode(buffer.getvalue()).decode()

    return {
        "status": "success",
        "image_base64": encoded
    }
