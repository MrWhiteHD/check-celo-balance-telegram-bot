FROM python:alpine
RUN apk update && \
    apk add --no-cache bash
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY celo_balance_bot.py /app
COPY /bot_data/accounts.json /bot_data/accounts.json
COPY /bot_data/celo_accounts.json /bot_data/celo_accounts.json
CMD [ "python", "./celo_balance_bot.py" ]
