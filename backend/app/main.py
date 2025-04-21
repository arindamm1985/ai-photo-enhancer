
from flask import Flask, request, jsonify
from flask_cors import CORS
from app.s3_client import upload_file
from app.tasks import enhance_photo_task
import os

app = Flask(__name__)
CORS(app)
@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['photo']
    model = request.form.get('model', 'real-esrgan')
    filename = image.filename
    filepath = f"/tmp/{filename}"
    image.save(filepath)
    upload_file(filepath, filename)
    task = enhance_photo_task.delay(filename, model)
    return jsonify({"task_id": task.id})

@app.route('/status/<task_id>')
def status(task_id):
    from celery.result import AsyncResult
    result = AsyncResult(task_id)
    return jsonify({"status": result.status, "result": result.result if result.status == 'SUCCESS' else None})
