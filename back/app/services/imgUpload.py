import boto3
import os
import uuid
from botocore.config import Config


s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def create_presigned_url(file_extension: str):
    key = f"uploads/{uuid.uuid4()}.{file_extension}"
    
    upload_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': key,
            'ContentType': f'image/{file_extension}'
        },
        ExpiresIn=3600
    )
    
    image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
    
    return upload_url, image_url