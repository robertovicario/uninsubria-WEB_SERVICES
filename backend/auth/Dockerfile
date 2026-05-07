FROM python:3.9-slim

WORKDIR /app

COPY ./backend/auth /app
COPY ./backend/utils /app/utils
COPY ./frontend /app/frontend

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
