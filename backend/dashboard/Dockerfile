FROM python:3.9-slim

WORKDIR /app

COPY backend/dashboard /app
COPY backend/utils /app/utils
COPY frontend /app/frontend

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
