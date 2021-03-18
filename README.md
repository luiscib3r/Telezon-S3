# Telezon S3

## Deploy your server

Working in this documentation ...

---

## Client example

### Python - Boto3

```python
import boto3

access_key_id = 'your_access_key_id'
secret_key = 'your_secret_key'

telezon_s3_url = 'https://your-instance.herokuapp.com'

s3 = boto3.client(
    's3', 
    aws_access_key_id=access_key_id, 
    aws_secret_access_key=secret_key, 
    endpoint_url=telezon_s3_url
)

s3.upload_file('bucket_name', 'filename_example.jpg', 'id_name_for_file')

s3.download_file('bucket_name', 'id_name_for_file', 'downloaded_filename.jpg')
```