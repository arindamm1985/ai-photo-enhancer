
from celery import Celery
from app.s3_client import upload_file, download_file, get_s3_url
from app.gpu_client import enhance_image_with_replicate
import os
import time
import requests
from smtplib import SMTP
from email.mime.text import MIMEText

broker_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery = Celery('photo_ai', broker=broker_url, backend=broker_url)

@celery.task
def enhance_photo_task(s3_key, model_name):
    temp_input = f"/tmp/{s3_key}"
    temp_output = f"/tmp/enhanced-{s3_key}"
    download_file(s3_key, temp_input)
    input_url = get_s3_url(s3_key)
    status_url = enhance_image_with_replicate(model_name, input_url)

    while True:
        res = requests.get(status_url, headers={"Authorization": f"Token {os.getenv('REPLICATE_API_TOKEN')}"})
        output = res.json()
        if output['status'] == 'succeeded':
            output_url = output['output']
            break
        elif output['status'] == 'failed':
            raise Exception("Enhancement failed")
        time.sleep(5)

    r = requests.get(output_url, stream=True)
    with open(temp_output, 'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

    enhanced_key = f"enhanced/{s3_key}"
    upload_file(temp_output, enhanced_key)
    notify_user(get_s3_url(enhanced_key))
    return get_s3_url(enhanced_key)

def notify_user(download_url):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_FROM")
    subject = os.getenv("EMAIL_SUBJECT", "Your enhanced image is ready!")
    body = f"Download your enhanced photo here: {download_url}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = email_to

    with SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(email_from, [email_to], msg.as_string())
