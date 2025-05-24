FROM python:3.10

WORKDIR /app
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
COPY data /app/data
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "server.py"]
