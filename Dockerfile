FROM python:3.11-slim

# Update system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean

WORKDIR /app

COPY main.py ./
COPY env ./
COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["python", "main.py"]
