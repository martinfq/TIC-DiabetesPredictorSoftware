FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-distutils \
    python3-setuptools \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
