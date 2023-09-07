FROM python:3.10.10

COPY . /app
WORKDIR /app

RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "-u", "./app.py"]