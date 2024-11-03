FROM python:3.12-alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    make

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /

EXPOSE 8000

CMD ["fastapi", "run", "--workers", "4", "app/main.py"]