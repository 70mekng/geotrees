import os
import json
from google.cloud import vision
from google.oauth2 import service_account


def ocr_google(image_url: str):
    # credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    # credentials = service_account.Credentials.from_service_account_file(credentials_path)
    
    credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    # print(f"DEBUG: GOOGLE_APPLICATION_CREDENTIALS_JSON: {creds_json}")
    credentials = service_account.Credentials.from_service_account_info(json.loads(credentials_json))
    
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image = vision.Image()
    image.source.image_uri = image_url
    
    response = client.text_detection(image=image)
    
    if response.error.message:
        raise Exception(response.error.message)
    
    texts = response.text_annotations
    if texts:
        return texts[0].description
    return ""