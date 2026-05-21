from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageOps
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

# OUTPUT
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")


# -----------------------------
# IMAGE LOADER SAFE
# -----------------------------
def load_image(url):
    try:
        if not url:
            return None
        r = requests.get(url, timeout=10)
        return Image.open(BytesIO(r.content)).convert("RGBA")
    except:
        return None


# -----------------------------
# CATEGORY BASE POSITION
# -----------------------------
def get_position(category, base_w, base_h, index):

    if category == "koltuk":
        return int(base_w * 0.15) + (index * 30), int(base_h * 0.55)

    if category == "masa":
        return int(base_w * 0.45), int(base_h * 0.50)

    if category == "aksesuar":
        return int(base_w * 0.70) + (index * 20), int(base_h * 0.60)

    return 100 + index * 120, int(base_h * 0.6)


# -----------------------------
# HOME
# -----------------------------
@app.get("/")
def home():
    return {"status": "AI Render V3 Ready"}


# -----------------------------
# MAIN RENDER ENGINE
# -----------------------------
@app.post("/render")
async def render(request: Request):

    data = await request.json()

    mode = data.get("mode", "2")
    room_url = data.get("roomImage")
    products = data.get("products", "")

    # -------------------------
    # ROOM IMAGE (ZORUNLU MODE 2)
    # -------------------------
    base = load_image(room_url)

    if base is None:
        base = Image.new("RGBA", (1400, 900), (235, 235, 235))

    base = base.resize((1400, 900))
    base_w, base_h = base.size

    # -------------------------
    # PRODUCT PARSE
    # -------------------------
    product_list = []
    if products:
        product_list = [p.strip() for p in products.split(",") if p.strip()]

    # -------------------------
    # PLACE PRODUCTS
    # -------------------------
    for i, item in enumerate(product_list):

        try:
            parts = item.split("|")

            url = parts[0]
            category = parts[1] if len(parts) > 1 else "genel"
            count = int(parts[2]) if len(parts) > 2 else 1

            for c in range(count):

                img = load_image(url)

                if img is None:
                    continue

                # SCALE
                scale = 0.25
                img = ImageOps.contain(img, (int(400 * scale), int(400 * scale)))

                x, y = get_position(category, base_w, base_h, c)

                base.paste(img, (x, y), img)

        except:
            continue

    # -------------------------
    # SAVE OUTPUT
    # -------------------------
    filename = f"{uuid.uuid4().hex}.png"
    file_path = os.path.join(OUTPUT_DIR, filename)

    base.save(file_path)

    image_url = f"https://ai-render-backend.onrender.com/static/{filename}"

    return {
        "status": "success",
        "mode": mode,
        "image_url": image_url
    }
