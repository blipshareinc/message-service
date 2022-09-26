FROM python:3.11.0rc1-alpine3.16

ARG user=appuser
ARG group=appuser
ARG uid=1001
ARG gid=1001

RUN apk update && \
    apk add sudo vlc alsa-utils alsa-utils-doc alsa-lib && \
    apk add alsaconf alsa-ucm-conf dbus pulseaudio pulseaudio-alsa

RUN addgroup -g ${gid} ${group} && \
    adduser -h /home/$user --disabled-password --gecos "" --uid ${uid} --ingroup ${group} $user && \
    adduser $user wheel && \
    echo '%wheel ALL=(ALL) ALL' > /etc/sudoers.d/wheel

COPY . /app

RUN chown $user /app

USER $user

WORKDIR /app

RUN python3 -m venv env && \
    . ./env/bin/activate && \
    pip install -r requirements.txt

ENV PYTHONPATH=/app:$PYTHONPATH
ENV PATH=/app/env/bin:$PATH
ENV DISPLAY=:0

EXPOSE $PORT

CMD ["/bin/sh", "-c", "gunicorn --workers ${WORKERS} --bind ${HOST}:${PORT} 'app:app'"]
