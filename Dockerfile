FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
EXPOSE $PORT

CMD gunicorn --workers 4 --bind 0.0.0.0:$PORT --timeout 120 app:create_app() 