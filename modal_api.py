import modal
import numpy as np
import cv2
from ocr import get_text

# Initialize Modal App
stub = modal.App("omni-llama-api")
secrets = modal.Secret.from_name("omni-secrets")

@stub.function(
    image=modal.Image.debian_slim()
    .apt_install("tesseract-ocr")  # Install Tesseract OCR inside Modal
    .pip_install("fastapi", "pytesseract", "Pillow", "llama-cpp-python", "requests")
)
def load_dependencies():
    """Load dependencies inside Modal environment"""
    import pytesseract
    from fastapi import FastAPI
    from io import BytesIO
    import base64
    from PIL import Image
    from llama_cpp import Llama
    import requests
    return pytesseract, FastAPI, BytesIO, base64, Image, Llama, requests

# Load dependencies inside Modal (Fixes the error)
pytesseract, FastAPI, BytesIO, base64, Image, Llama, requests = load_dependencies()

# Initialize FastAPI inside Modal
app = FastAPI()

@app.post("/process-image")
async def process_image(data: dict):
    """Receives a cropped image, extracts text, and sends event to Google Calendar"""
    base64_image = data.get("image")
    token = data.get("token")

    # Convert image from Base64
    image_bytes = base64.b64.decode(base64_image)
    image = cv2.imdecode(np.frombuffer(image_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)

    # Extract text from image
    extracted_text = get_text(image)

    # Use Llama 3 to extract event details
    response = Llama(model_path="/models/llama-3-8b.Q4_K_M.gguf").create_completion(
        f"Extract event details: {extracted_text}"
    )

    # Prepare event data
    event_data = response["choices"][0]["text"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Send event to Google Calendar API
    requests.post("https://www.googleapis.com/calendar/v3/calendars/primary/events", json=event_data, headers=headers)

@stub.function()
@modal.asgi_app()
def fastapi_app():
    """Deploy FastAPI inside Modal"""
    return app
