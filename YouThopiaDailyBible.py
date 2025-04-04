import telebot
import requests
import schedule
import threading
import time

# Replace with your bot's token from BotFather
TOKEN = "7873297390:AAEWojFXWfSxp7OeAhRkY1xwE4H_A6m5i_8"
bot = telebot.TeleBot(TOKEN)
CHAT_ID = "-1001904672000", "-1002405018686" # Replace with the actual group ID

# Function to get a random Bible verse
def get_random_verse():
    url = "https://bible-api.com/?random=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{data['reference']}\n\n{data['text']}"
    else:
        return "Sorry, I couldn't fetch a scripture right now."

# Function to send an automatic Bible verse every morning
def send_morning_verse():
    print("Sending Morning Verse")
    verse = get_random_verse()
    bot.send_message(CHAT_ID, f"Hey, Good Morning! Here is Today's  Bible verse📖:\n\n{verse}")


# Schedule the message to run every day at 06:00 AM
schedule.every().day.at("06:00").do(send_morning_verse)


# Function to run the schedule in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every 60 seconds

# Start the scheduler in a new thread
threading.Thread(target=run_scheduler, daemon=True).start()

# Command to send a random Bible verse manually
@bot.message_handler(commands=["verse"])
def send_verse(message):
    bot.reply_to(message, get_random_verse())


print("Bot is running....")
bot.polling(non_stop=True, timeout=60)
