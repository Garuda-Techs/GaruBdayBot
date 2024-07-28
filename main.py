from typing import Final
from telegram import Update
from telegram.ext import Application, CallbackContext, ContextTypes
import pandas as pd
import requests
from datetime import datetime
import logging
import io
import asyncio

TOKEN = '6858348326:AAFpoAlVINlW08nVikkwGS8jFDV1bKgKPQM'
BOT_USERNAME: Final = '@GaruBdayBot'
CSV_URL = "https://raw.githubusercontent.com/Garuda-Techs/GaruBdayBot/main/birthdays.csv"
CHAT_ID = '-1002175948359'  # Replace with your actual chat ID
TOPIC_THREAD_ID = '4' # Replace with your actual topic thread ID

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_birthdays(application: Application):
    today = datetime.now().strftime('%d/%m')
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()  # Ensure we notice bad responses
        df = pd.read_csv(io.StringIO(response.text))

        for index, row in df.iterrows():
            if today == row['Birthday']:
                await application.bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"Happy Birthday {row['Name']}!",
                    message_thread_id=TOPIC_THREAD_ID
                )
    except Exception as e:
        logger.error(f"Failed to fetch or process CSV: {e}")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')

async def main():
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Errors
    app.add_error_handler(error)

    # Initialize and start the application, then check birthdays
    await app.initialize()
    await app.start()
    await check_birthdays(app)
    await app.stop()

if __name__ == '__main__':
    asyncio.run(main())
