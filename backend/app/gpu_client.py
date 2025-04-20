
import requests
import os

REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")
REAL_ESRGAN_MODEL = "tencentarc/real-esrgan"
HDRNET_MODEL = "google/hdrnet"
HEADERS = {"Authorization": f"Token {REPLICATE_TOKEN}"}

def enhance_image_with_replicate(model, image_url):
    model_version = REAL_ESRGAN_MODEL if model == "real-esrgan" else HDRNET_MODEL
    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers=HEADERS,
        json={"version": model_version, "input": {"image": image_url}}
    )
    prediction = response.json()
    return prediction["urls"]["get"]
