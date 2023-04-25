import json
import uuid
from uuid import UUID
from flask_sqlalchemy import Model
from io import BytesIO
from google.cloud import storage
from google.auth.credentials import Credentials

class CustomJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that can handle UUID objects.
    """

    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)


def to_json(obj):
    """
    Serialize a SQLAlchemy model instance to JSON.
    """
    if isinstance(obj, list):
        return [to_json(item) for item in obj]
    elif isinstance(obj, Model):
        data = {}
        for column in obj.__table__.columns:
            value = getattr(obj, column.name)
            if isinstance(value, Model):
                data[column.name] = to_json(value)
            else:
                data[column.name] = value
        return data
    # else:
    #     return {}
        # raise TypeError(
        #     "Object of type '%s' is not JSON serializable" %
        #     type(obj).__name__)

def upload_image(image_bytes):
    creds = Credentials.from_service_account_file('key.json')
    image_bytes = b''.join([bytes([x]) for x in image_bytes])
    client = storage.Client()
    bucket = client.bucket("jonathan_bucket_1234")
    file_name = str(uuid.uuid4()) + '.jpg'
    blob = bucket.blob('images/' + file_name)
    blob.upload_from_file(BytesIO(image_bytes), content_type='image/jpeg')
    print('Image uploaded to Google Cloud with file name:', file_name)
    return blob