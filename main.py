from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import requests
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

# OPENAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# HOME
@app.get("/")
def home():
    return {"status": "AI Render Engine Ready"}

# MAIN RENDER
@app.post("/render")
async def render(request: Request):

    try:

        data = await request.json()

        room_type = data.get("roomType", "modern office")
        style = data.get("style", "modern")
        sqm = data.get("sqm", "35")

        products = data.get("products", "")

        if not os.getenv("OPENAI_API_KEY"):

            return {
                "error": "OPENAI_API_KEY missing"
            }

        prompt = f"""
        Create a photorealistic luxury office interior.

        Room type:
        {room_type}

        Style:
        {style}

        Room size:
        {sqm} square meters.

        Use these furniture references:
        {products}

        Realistic lighting,
        luxury materials,
        architectural render,
        ultra realistic,
        interior design photography.
        """

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1536x1024"
        )

        image_base64 = result.data[0].b64_json

        import base64

        filename = f"{uuid.uuid4().hex}.png"

        file_path = os.path.join(OUTPUT_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image_base64))

        image_url = f"https://ai-render-backend.onrender.com/static/{filename}"

        return {
            "status": "success",
            "image_url": image_url
        }

    except Exception as e:

        return {
            "error": str(e)
        }
if not os.getenv("OPENAI_API_KEY"):
    return {
        "error": "OPENAI_API_KEY missing"
    }
    
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1536x1024"
    )

    image_base64 = result.data[0].b64_json

    import base64

    filename = f"{uuid.uuid4().hex}.png"
    file_path = os.path.join(OUTPUT_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(base64.b64decode(image_base64))

    image_url = f"https://ai-render-backend.onrender.com/static/{filename}"

    return {
        "status": "success",
        "image_url": image_url
    }
