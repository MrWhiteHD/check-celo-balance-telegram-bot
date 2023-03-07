import json
import requests
import telebot
import schedule
import time
import threading

# Set the API_TOKEN in the docker_compose.yml or paste it in the comment below and uncomment the line
# API_TOKEN = "000000000"
bot = telebot.TeleBot(API_TOKEN)

# Welcome Message from Bot or triggered with /start command
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, f"Hi <b>{message.chat.username}</b>,\nim your personal celo balance alert bot.\n\nIm Tracking the Celo Oracle balances for u.\n\nPress /start_alerting to get notifications when the balance of an Celo Oracle is below 5 Celo\n\nPress /stop_alerting to stop notifications when the balance of an Celo Oracle is below 5 Celo\n\nPress /check_balance to get current balances of Celo Oracles", parse_mode='HTML')

# /start_alerting command to write user_id and user_name in the users.json, so they can get a notification when an Oracle balance drop below a given value. NOTE: The username is not required and can be deleted, just for own purposes
@bot.message_handler(commands=['start_alerting'])
def start_alerting(message):
    # Get the name and user ID from the command arguments
    name = message.chat.username
    user_id = message.chat.id
    # Load the accounts JSON file
    with open('/bot_data/users.json', 'r') as f:
        data = json.load(f)
    user_ids = [user['user_id'] for user in data['users']]
    if user_id in user_ids:
        bot.reply_to(message, f"The alerting is already turned on.")
        return
    # Create a new user object
    new_user = {"Name": name, "user_id": user_id}
    # Append the new user to the accounts list
    data["users"].append(new_user)
    # Save the updated users.json file
    with open('/bot_data/users.json', 'w') as f:
        json.dump(data, f)
        bot.reply_to(message, f"The alerting is turned on and you will get notifications.")

# /stop_alerting command to delete user_id and user_name in the "users.json", so they dont get any notifications anymore
@bot.message_handler(commands=['stop_alerting'])
def stop_alerting(message):
    # Get the name and user ID from the command arguments
    user_id = message.chat.id
    # Load the accounts JSON file
    with open('/bot_data/users.json', 'r') as f:
        data = json.load(f)
        # Check if the user ID exists in the file
        user_index = None
        for i, user in enumerate(data['users']):
            if user['user_id'] == user_id:
                user_index = i
            break
        if user_index is None:
            bot.reply_to(message, f"The alerting is already turned off.")
            return
        # Delete the user object from the "users.json" list
        del data['users'][user_index]
        with open('/bot_data/users.json', 'w') as f:
            json.dump(data, f)
        bot.reply_to(message, f"The alerting is turned off and you won't get any notifications anymore.")

# /check_balance commad to trigger manually a api request for all Celo addresses from "celo_accounts.json"
@bot.message_handler(commands=['check_balance'])
def check_Balance(message):
    # Get the name and celo_address from celo_accounts.json
    with open("/bot_data/celo_accounts.json", "r") as f:
        data = json.load(f)
        for item in data["accounts"]:     
            name = item['Name']
            celo_address = item['Address']
            # Get the balance from each item in celo_accounts.json and trigget a api request
            api_url = f"https://explorer.celo.org/mainnet/api?module=account&action=balance&address={celo_address}"
            response = requests.get(api_url)
            data = response.json()
            # Extract the balance from response data
            result = int(data['result'])
            # Calculate the balance from wei 
            balance = (result / 1000000000000000000)
            # Format the balance result and add " CELO"
            balance_formatted = "{:.4f}".format(balance)+' CELO'
            # Reply to user with name of address and the current balance
            message_reply = f"The balance of <b>{name}</b>\nis <b>{balance_formatted}</b>"
            bot.reply_to(message, message_reply, parse_mode='HTML')

# Run a api request, get current balance and create a alert message. The function is scheduled to run at a regular interval from the schedule.every().minutes.do() method
def check_api():
    with open("/bot_data/celo_accounts.json", "r") as f:
        data = json.load(f)
        for item in data["accounts"]:
            name_check = item['Name']
            celo_address = item['Address']
            api_url = f"https://explorer.celo.org/mainnet/api?module=account&action=balance&address={celo_address}"
            response = requests.get(api_url)
            data = response.json()
            result = int(data['result'])
            balance = (result / 1000000000000000000)
            balance_formatted_check = "{:.4f}".format(balance)+' CELO'
            message_text = f"ALERT: The balance of <b>{name_check}</b>\nis <b>{balance_formatted_check}</b>"
            if balance < 5:
                with open("/bot_data/users.json", "r") as f:
                    data = json.load(f)
                    for users in data["users"]:
                        user_id = users['user_id']
                        bot.send_message(user_id, message_text, parse_mode='HTML')

# Schedule "check_api" command in a interval of 720 minutes (12 hours) since the Oracles fees are very low. Can be adapted, if you want to track Celo addresses.
schedule.every(720).minutes.do(check_api)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Threading for the schedule, since the bot runs in a loop and no other functions would be started
t = threading.Thread(target=run_schedule)
t.start()

# Telebot function to run Telegram bot
bot.polling()
