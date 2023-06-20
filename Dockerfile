FROM python:3.10-alpine

RUN apk update && \
    apk add --upgrade gcc g++ linux-headers

RUN python3 -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
