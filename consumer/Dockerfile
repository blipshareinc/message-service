FROM python:3.11.0rc1-alpine3.16

ARG user=appuser
ARG group=appuser
ARG uid=1001
ARG gid=1001

RUN apk update && \
    apk add vlc alsa-utils alsa-utils-doc alsa-lib alsaconf alsa-ucm-conf

RUN addgroup -g ${gid} ${group} && \
    adduser --disabled-password --gecos "" --uid ${uid} --ingroup ${group} $user

COPY . /app

RUN chown appuser /app

USER appuser

WORKDIR /app

RUN python3 -m venv env && \
    . ./env/bin/activate && \
    pip install -r requirements.txt

ENV PYTHONPATH=/app:$PYTHONPATH
ENV PATH=/app/env/bin:$PATH

EXPOSE $PORT

CMD ["/bin/sh", "-c", "gunicorn --workers ${WORKERS} --bind ${HOST}:${PORT} 'app:app'"]
