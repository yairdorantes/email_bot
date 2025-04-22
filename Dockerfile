FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /usr/src/app/main.py

# Optional: Disable buffering so you can see logs immediately
ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "main.py"]
