FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# .envファイルをコンテナ内にコピー
COPY .env .env

CMD ["python", "app/main.py"]
