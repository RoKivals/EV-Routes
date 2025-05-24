FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir fastapi[standard] && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/src
ENV DATABASE_URL=postgresql+asyncpg://fastapi:secret@postgres:5432/fastapi_dev

CMD ["python", "main.py"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]