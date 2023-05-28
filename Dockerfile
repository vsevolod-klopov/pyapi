FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE=1


ENV PYTHONUNBUFFERED=1



COPY requirements.txt .


RUN python -m pip install -r requirements.txt


WORKDIR /app




CMD ["gunicorn", "--bind", "0.0.0.0:80", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
