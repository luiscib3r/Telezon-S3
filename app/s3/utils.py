from starlette.requests import Request

from app.models.bucket import Bucket
from app.s3.awssig import AWSSigV4Verifier, InvalidSignatureError


async def aws_sig_verify(bucket: Bucket, request: Request):
    body = await request.body()
    headers = dict(**request.headers)
    headers['X-Amz-Date'] = headers.get('x-amz-date', '')
    path = str(request.url).replace(str(request.base_url), '/')

    v = AWSSigV4Verifier(
        request_method=request.method,
        uri_path=path,
        query_string=str(request.query_params),
        headers=headers,
        body=body,
        region="us-east-1",
        service="s3",
        key_mapping={bucket.owner.access_key_id: bucket.owner.secret_key},
        timestamp_mismatch=None
    )
    try:
        v.verify()
        return True
    except InvalidSignatureError as e:
        print('Invalid signature: %s', e)
    except Exception as e:
        print('Unable to verify request: %s', e)
