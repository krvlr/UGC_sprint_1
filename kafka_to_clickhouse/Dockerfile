FROM python:3.10.2

WORKDIR /opt/app

COPY requirements.txt requirements.txt
COPY wait-for-it.sh wait-for-it.sh

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x wait-for-it.sh

ENTRYPOINT ["./wait-for-it.sh", "clickhouse-node1:9000", "--", "python", "app.py"]