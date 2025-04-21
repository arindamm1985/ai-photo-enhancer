from flask import Flask, request, jsonify
from flask_cors import CORS
from app.s3_client import upload_file, get_s3_url
from app.gpu_client import enhance_image_with_replicate
import os, time, requests

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        return jsonify({"error": "No photo provided"}), 400

    image = request.files['photo']
    model = request.form.get('model', 'real-esrgan')
    filename = image.filename
    filepath = f"/tmp/{filename}"
    image.save(filepath)

    # Upload original to S3
    upload_file(filepath, filename)
    input_url = get_s3_url(filename)

    # Send to Replicate and poll for result
    status_url = enhance_image_with_replicate(input_url)
    while True:
        res = requests.get(status_url, headers={"Authorization": f"Token {os.getenv('REPLICATE_API_TOKEN')}"})
        data = res.json()
        if data['status'] == 'succeeded':
            output_url = data['output']
            break
        elif data['status'] == 'failed':
            return jsonify({"error": "Enhancement failed"}), 500
        time.sleep(3)

    # Download and re-upload enhanced image
    response = requests.get(output_url)
    enhanced_path = f"/tmp/enhanced-{filename}"
    with open(enhanced_path, "wb") as f:
        f.write(response.content)

    enhanced_key = f"enhanced/{filename}"
    upload_file(enhanced_path, enhanced_key)

    return jsonify({
        "status": "success",
        "enhanced_url": get_s3_url(enhanced_key)
    })
