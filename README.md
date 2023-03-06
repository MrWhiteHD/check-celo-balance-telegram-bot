# This documentation is WIP and will be improved.
Documentation for the Telegram celo alert bot.

## 1. Create BOT and API-Key in Telegram
### Open Telegram and search for "@BotFather"
- Create a new Bot with "/newbot".
- First you need to name your Bot.
- Second you need to give your Bot a username like "[NAME]Bot" or "[NAME]_bot" e.g. TestBot or Test_bot. The name must be unique since its the Telegram username.
- You can set your profile picture and infos in the BotFather menu.

## 2. Adapt code to run your own bot
### Insert your API-KEY from @BotFather 
- Paste it as value into the [docker_compose.yaml](https://github.com/MrWhiteHD/check-celo-balance-telegram-bot/blob/main/docker_compose.yaml)
- OR you can adapt API_TOKEN in the [celo_balane_bot.py](https://github.com/MrWhiteHD/check-celo-balance-telegram-bot/blob/main/celo_balane_bot.py)

## 3. Important things before start
- The file [users.json](https://github.com/MrWhiteHD/check-celo-balance-telegram-bot/blob/main/users.json) store all user data. It is recommended to run the bot in a container, but you need to mount the file in an external storage, and adapt the file path in the code so the user data dont get lost after a container update.
- Add all your Celo addresses into the file [celo_accounts.json](https://github.com/MrWhiteHD/check-celo-balance-telegram-bot/blob/main/celo_accounts.json) so the bot can make api requests for the addresses.
- The bot is using [Celo Explorer](https://explorer.celo.org/) for the api requests.

## 4. Run the bot and have fun
- Run the Bot in a container or on a local machine (im using for testing the local machine before i create docker image) and enjoy.

NOTE: The documentation is still WIP and will be improved with time
