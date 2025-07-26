FROM python:3.11-slim

WORKDIR /Ultron

RUN apt-get update && apt-get install -y \
    python3-dev \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "run.py"]
