from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API aktif"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/render")
async def render(request: Request):

    data = await request.json()

    return {
        "status": "ok",
        "message": "API çalışıyor"
    }
