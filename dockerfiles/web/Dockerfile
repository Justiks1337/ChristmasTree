FROM python:3.13-slim

COPY web_django/requirements.txt .

RUN python3 -m pip install --no-cache-dir --no-warn-script-location --upgrade pip \
&& python3 -m pip install --no-cache-dir --no-warn-script-location --user -r requirements.txt

COPY web_django/ .

RUN python3 manage.py makemigrations