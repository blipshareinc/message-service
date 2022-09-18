FROM python:3.11.0rc1-alpine3.16

RUN apk update

COPY . /app

WORKDIR /app

RUN python3 -m venv env && \
    . ./env/bin/activate && \
    pip install -r requirements.txt

ENV PYTHONPATH=/app:$PYTHONPATH
ENV PATH=/app/env/bin:$PATH

EXPOSE $PORT

CMD ["/bin/sh", "-c", "gunicorn --workers ${WORKERS} --bind ${HOST}:${PORT} 'app:app'"]
