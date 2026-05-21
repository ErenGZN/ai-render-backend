from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image
import requests
from io import BytesIO
import uuid
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Output klasörü
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Static serve (üretilen görselleri URL ile açmak için)
app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")


# ---------------------------
# IMAGE LOAD SAFE FUNCTION
# ---------------------------
def load_image(url):
    try:
        if not url:
            return None
        r = requests.get(url, timeout=10)
        return Image.open(BytesIO(r.content)).convert("RGBA")
    except:
        return None


# ---------------------------
# HOME
# ---------------------------
@app.get("/")
def home():
    return {"status": "AI Render Engine V3 Active"}


# ---------------------------
# RENDER ENGINE
# ---------------------------
@app.post("/render")
async def render(request: Request):

    data = await request.json()

    room_url = data.get("roomImage")
    products = data.get("products", "")

    # BACKGROUND
    base = load_image(room_url)

    if base is None:
        base = Image.new("RGBA", (1200, 800), (235, 235, 235))

    base = base.resize((1200, 800))

    # PRODUCT LIST
    product_list = []
    if products:
        product_list = [p.strip() for p in products.split(",") if p.strip()]

    # SIMPLE LAYOUT ENGINE
    x = 80
    y = int(base.size[1] * 0.55)

    max_per_row = 4
    count = 0

    for url in product_list:

        img = load_image(url)

        if img is None:
            continue

        # SCALE (dinamik)
        scale = 0.25
        w, h = img.size
        img = img.resize((int(w * scale), int(h * scale)))

        base.paste(img, (x, y), img)

        x += img.size[0] + 20
        count += 1

        if count % max_per_row == 0:
            x = 80
            y += 220

    # SAVE IMAGE
    filename = f"{uuid.uuid4().hex}.png"
    file_path = os.path.join(OUTPUT_DIR, filename)

    base.save(file_path)

    # PUBLIC URL
    image_url = f"https://ai-render-backend.onrender.com/static/{filename}"

    return {
        "status": "success",
        "image_url": image_url,
        "product_count": len(product_list)
    }
