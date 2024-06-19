from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import pandas as pd
import requests
from datetime import date, datetime, time
import logging
import asyncio



TOKEN = '6858348326:AAFpoAlVINlW08nVikkwGS8jFDV1bKgKPQM'
BOT_USERNAME = Final = '@GaruBdayBot'
# before you uncomment the line, add the csv file for the birthdays into the github repo
# CSV_URL =  "https://raw.githubusercontent.com/Garuda-Techs/GaruBdayBot/birthdays.csv"
today = date.today()

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am GaruBday Bot!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! GaruBdayBot Help command?')

    
async def check_birthdays(context: CallbackContext):
    today = datetime.now().strftime('%d/%m')
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()  # Ensure we notice bad responses
        df = pd.read_csv(pd.compat.StringIO(response.text))

        for index, row in df.iterrows():
            if today == row['Birthday']:
                await context.bot.send_message(chat_id=context.job.chat_id, text=f"Happy Birthday {row['Name']}!")
    except Exception as e:
        logger.error(f"Failed to fetch or process CSV: {e}")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Errors
    app.add_error_handler(error)

    # Schedule the birthday check function to run daily at a specific time (e.g., midnight)
    job_queue = app.job_queue
    job_queue.run_daily(check_birthdays, time=time(0, 0), name="birthday_check", chat_id='YOUR_CHAT_ID')

    print('Polling...')
    app.run_polling(poll_interval=3)
    