# Telezon S3

Telezon S3 es un servicio de almacenamiento compatible con la API de Amazon S3 que utiliza Telegram como backend de almacenamiento. Permite almacenar y recuperar archivos utilizando clientes S3 estándar.

## Despliegue con Docker

La forma más sencilla de ejecutar Telezon S3 es utilizando Docker Compose:

1. Clona el repositorio
2. Copia el archivo de variables de entorno:

```bash
cp .env.example .env
```

3. Configura las variables en el archivo `.env`
4. Inicia los servicios:

```bash
docker-compose up -d
```

El servicio estará disponible en `http://localhost:8000`

## Documentación de la API

La documentación interactiva de la API está disponible a través de Swagger UI. Puedes acceder a ella en:

```
http://localhost:8000/docs
```

## Requisitos para desarrollo

- Python 3.12+
- Poetry
- Docker y Docker Compose
- Una cuenta o bot de Telegram
- Un canal de Telegram

## Configuración

1. Clona el repositorio
2. Copia el archivo `.env.example` a `.env` y configura las variables de entorno:

```bash
cp .env.example .env
```

### Variables de Entorno Importantes

```env
# Configuración del Servidor
PROJECT_NAME='Telezon S3'
PORT=8000
SECRET_KEY=your_secret_key

# Configuración de MongoDB
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASSWORD=your_password
DATABASE_NAME=TelezonS3

# Configuración de Telegram
BOT_TOKEN=your_bot_token
CID=your_channel_id
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
SESSION_STRING=your_session_string
```

### Variables de Entorno para Usuario Administrador

El sistema permite configurar un usuario administrador inicial a través de variables de entorno:

```env
INITIAL_ADMIN_USER=admin
INITIAL_ADMIN_PASSWORD=admin
```

Estas credenciales se utilizarán para crear automáticamente el primer usuario administrador en el sistema durante la inicialización de la base de datos.

## Desarrollo

1. Instala las dependencias:

```bash
poetry install
```

2. Inicia el servidor en modo desarrollo:

```bash
make dev
```

### Configuración del Bot y Canal de Telegram

1. Configura el almacenamiento usando `pyrogram` (Recomendado):

```bash
make setup_account_storage
```

2. Configura el almacenamiento usando `python-telegram-bot` (No recomendado):

```bash
make setup_bot_storage
```

## Uso

### Cliente Python (boto3)

```python
import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id='your_access_key_id',
    aws_secret_access_key='your_secret_key',
    endpoint_url='http://localhost:8000'  # O tu URL de producción
)

# Subir archivo
s3.upload_file('archivo_local.txt', 'nombre_bucket', 'nombre_destino.txt')

# Descargar archivo
s3.download_file('nombre_bucket', 'nombre_destino.txt', 'archivo_descargado.txt')
```

### Script de Subida Rápida

El proyecto incluye un script de utilidad para subir archivos:

```bash
poetry run python upload_file.py \
 --access-key-id tu_access_key_id \
 --secret-key tu_secret_key \
 --bucket-name nombre_bucket \
 --input-path archivo_local.txt \
 --output-path nombre_destino.txt
```

## Comandos Make Disponibles

- `make dev`: Inicia el servidor en modo desarrollo
- `make run`: Inicia el servidor en modo producción
- `make format`: Formatea el código usando ruff
- `make setup_bot_storage`: Configura el almacenamiento del bot
- `make setup_account_storage`: Configura el almacenamiento de la cuenta
- `make export`: Exporta las dependencias a requirements.txt

## Características

- Compatible con la API de Amazon S3
- Utiliza Telegram como backend de almacenamiento
- Soporte para operaciones básicas de S3 (upload/download)
- Integración con clientes S3 estándar

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos.

## Licencia

MIT
