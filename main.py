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

def load_image(url):
    r = requests.get(url)
    return Image.open(BytesIO(r.content)).convert("RGBA")

def resize_product(img, scale):
    w, h = img.size
    return img.resize((int(w * scale), int(h * scale)))

@app.get("/")
def home():
    return {"status": "v2.2 compositing engine active"}

@app.post("/render")
async def render(request: Request):

    data = await request.json()

    room_url = data.get("roomImage")
    products = data.get("products", [])

    # 1. Oda görseli
    base = load_image(room_url)

    base_w, base_h = base.size

    # 2. ürünleri parse et (basit CSV varsayımı)
    product_list = products.split(",")

    # 3. sahte yerleşim algoritması
    x_offset = 50
    y_offset = int(base_h * 0.6)

    for i, p in enumerate(product_list):

        try:
            img = load_image(p.strip())

            # ölçek (ürün sayısına göre küçült)
            scale = 0.3 - (i * 0.05)
            if scale < 0.15:
                scale = 0.15

            img = resize_product(img, scale)

            base.paste(img, (x_offset, y_offset), img)

            x_offset += img.size[0] + 20

        except:
            continue

    # 4. output buffer
    import base64
    from io import BytesIO

    buffer = BytesIO()
    base.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode()

    return {
        "status": "success",
        "message": "real composited render",
        "image_base64": encoded
    }
