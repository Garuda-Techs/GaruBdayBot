from typing import Final
from telegram import Update
from telegram.ext import Application, CallbackContext, ContextTypes
import pandas as pd
import requests
from datetime import datetime, timedelta
import logging
import io
import asyncio
from dotenv import load_dotenv
import os
import gspread
from google.oauth2.service_account import Credentials

# Get environment variables
load_dotenv()

TOKEN = "8314571423:AAFRNvR4a7FprR3Sv2Z57mcLdKw9feicXYo" #os.getenv('BOT_TOKEN')
BOT_USERNAME: Final = "'@GarudaBdayBot'
# CHAT_ID = "-1002218572340" # Testing: HC Techies Chat
# CHAT_ID = '-1002175948359'  # Production: Garuda House Chat
CHAT_ID = '-1002993620001' # Testing: HC Techies Chat 25/26
TOPIC_THREAD_ID = '12' # Birthday Subtopic
SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1H684nLTxJn2vQOCR1Zhv1CiqNAt535Q9yhHQCGaXqIw/edit?pli=1&gid=2135567390#gid=2135567390'

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_birthdays(application: Application):
    today = (datetime.now() + timedelta(hours=8)).strftime('%d/%m') # Add 8 hours to work around UTC timings
    try:
        # Initialise and read from Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = Credentials.from_service_account_file("service-account-key.json", scopes=scope)
        gc = gspread.authorize(credentials) # Authenticate and initialize the gspread client
        spreadsheet = gc.open_by_url(SPREADSHEET_URL)
        sheet = spreadsheet.get_worksheet(0)
        data = sheet.get_all_values() # Get all values in the sheet
        df = pd.DataFrame(data[1:], columns=data[0]) # Convert the data to a Pandas DataFrame

        for index, row in df.iterrows():
            if today == row['Birthday']:
                await application.bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"Happy Birthday {row['Name']}!",
                    message_thread_id=TOPIC_THREAD_ID
                )
    
    except Exception as e:
        logger.error(f"Failed to fetch or process Google Sheet: {e}")

"""
CSV_URL = "https://raw.githubusercontent.com/Garuda-Techs/GaruBdayBot/main/birthdays.csv"
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
"""

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
