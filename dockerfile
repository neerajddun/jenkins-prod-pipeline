FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt . 

RUN apt update && apt upgrade -y && rm -rf /var/lib/apt/lists*

COPY .  . 

RUN pip install --no-cache-dir -r requirements.txt 

CMD ["python","app.py"]