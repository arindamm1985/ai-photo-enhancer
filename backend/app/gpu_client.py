import requests
import os

REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")
MODEL_VERSION = "7a442900c289c0f63a4c50910f022ca42f59ec6f492eeb6fda10fdf93d12c530"
HEADERS = {
    "Authorization": f"Token {REPLICATE_TOKEN}",
    "Content-Type": "application/json"
}

def enhance_image_with_replicate(image_url):
    if not REPLICATE_TOKEN:
        raise ValueError(" Missing REPLICATE_API_TOKEN in environment.")

    try:
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers=HEADERS,
            json={
                "version": MODEL_VERSION,
                "input": {"image": image_url}
            }
        )
        response.raise_for_status()
        prediction = response.json()

        # Return the status URL to poll
        return prediction["urls"]["get"]

    except requests.exceptions.HTTPError as http_err:
        print("Replicate API Error:", response.status_code, response.text)
        raise RuntimeError(f"Replicate API Error: {response.status_code} - {response.text}")
    except Exception as err:
        print("Unexpected error while calling Replicate:", str(err))
        raise RuntimeError(f"Unexpected error: {str(err)}")
