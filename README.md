# Telezon S3

Telezon S3 is a storage service compatible with Amazon S3 API that uses Telegram as a storage backend. It allows storing and retrieving files using standard S3 clients.

## Docker Deployment

The easiest way to run Telezon S3 is using Docker Compose:

1. Clone the repository
2. Copy the environment variables file:

```bash
cp .env.example .env
```

3. Configure the variables in the `.env` file
4. Start the services:

```bash
docker-compose up -d
```

The service will be available at `http://localhost:8000`

## API Documentation

The interactive API documentation is available through Swagger UI. You can access it at:

```
http://localhost:8000/docs
```

## Development Requirements

- Python 3.12+
- Poetry
- Docker and Docker Compose
- A Telegram account or bot
- A Telegram channel

## Configuration

1. Clone the repository
2. Copy the `.env.example` file to `.env` and configure the environment variables:

```bash
cp .env.example .env
```

### Important Environment Variables

```env
# Server Configuration
PROJECT_NAME='Telezon S3'
PORT=8000
SECRET_KEY=your_secret_key

# MongoDB Configuration
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASSWORD=your_password
DATABASE_NAME=TelezonS3

# Telegram Configuration
BOT_TOKEN=your_bot_token
CID=your_channel_id
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
SESSION_STRING=your_session_string
```

### Initial Admin User

The system allows configuring an initial admin user through environment variables:

```env
INITIAL_ADMIN_USER=admin
INITIAL_ADMIN_PASSWORD=admin
```

These credentials will be used to automatically create the first admin user in the system during database initialization.

## Development

1. Install dependencies:

```bash
poetry install
```

2. Start the server in development mode:

```bash
make dev
```

### Telegram Bot and Channel Setup

1. Configure storage using `pyrogram` (Recommended):

```bash
make setup_account_storage
```

2. Configure storage using `python-telegram-bot` (Not recommended):

```bash
make setup_bot_storage
```

## Usage

### Python Client (boto3)

```python
import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id='your_access_key_id',
    aws_secret_access_key='your_secret_key',
    endpoint_url='http://localhost:8000'  # Or your production URL
)

# Upload file
s3.upload_file('local_file.txt', 'bucket_name', 'destination_name.txt')

# Download file
s3.download_file('bucket_name', 'destination_name.txt', 'downloaded_file.txt')
```

### Quick Upload Script

The project includes a utility script for uploading files:

```bash
poetry run python upload_file.py \
 --access-key-id your_access_key_id \
 --secret-key your_secret_key \
 --bucket-name bucket_name \
 --input-path local_file.txt \
 --output-path destination_name.txt
```

## Available Make Commands

- `make dev`: Start server in development mode
- `make run`: Start server in production mode
- `make format`: Format code using ruff
- `make setup_bot_storage`: Set up bot storage
- `make setup_account_storage`: Set up account storage
- `make export`: Export dependencies to requirements.txt

## Features

- Compatible with Amazon S3 API
- Uses Telegram as storage backend
- Support for basic S3 operations (upload/download)
- Integration with standard S3 clients

## Contributing

Contributions are welcome. Please open an issue to discuss proposed changes.

## License

MIT
