import boto3
import typer


def main(
    s3_url: str = typer.Argument("http://127.0.0.1:8000"),
    access_key_id: str = typer.Option(..., prompt=True),
    secret_key: str = typer.Option(..., prompt=True),
    bucket_name: str = typer.Option(..., prompt=True),
    input_path: str = typer.Option(..., prompt=True),
    output_path: str = typer.Option(..., prompt=True),
):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_key,
        endpoint_url=s3_url,
    )

    s3.upload_file(input_path, bucket_name, output_path)

    s3.download_file(bucket_name, output_path, input_path)


if __name__ == "__main__":
    typer.run(main)
