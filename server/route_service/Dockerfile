FROM python:3.13.3-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .

RUN pip install --no-cache-dir fastapi[standard] && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004", "--reload"]