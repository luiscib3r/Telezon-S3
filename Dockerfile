FROM python:3.8

COPY poetry.lock /
COPY pyproject.toml .
RUN pip install poetry && \
    poetry config settings.virtualenvs.create false && \
    poetry install

COPY . /

# Not expose for heroku deploy
# EXPOSE 8000

CMD gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT