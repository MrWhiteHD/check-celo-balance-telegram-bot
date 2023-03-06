FROM python:alpine
RUN apk update && \
    apk add --no-cache bash
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD [ "python", "./celo_balance_bot.py" ]
