FROM python:3.13-slim

RUN mkdir /telegram
COPY telegram_bot/requirements.txt /telegram

RUN python3 -m pip install --no-cache-dir --no-warn-script-location --upgrade pip \
&& python3 -m pip install --no-cache-dir --no-warn-script-location --user -r /telegram/requirements.txt

COPY telegram_bot /telegram