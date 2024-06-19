from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pandas as pd
from datetime import datetime
from datetime import date
import logging
import asyncio


TOKEN = '6858348326:AAFpoAlVINlW08nVikkwGS8jFDV1bKgKPQM'
BOT_USERNAME = Final = '@GaruBdayBot'
today = date.today()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    while True:
        #Check if current date time == midnight if it does then actually do this if not go to sleep for x amount of time then check agoin
        await update.message.reply_text('Hello! I am GaruBday Bot!')
        task = asyncio.create_task(continuous_function(update))
        await task
        print(task.result())
        await update.message.reply_text(task.result())




async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! GaruBdayBot Help command?')
    #decision tree, ask for name, check for
    
# async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await update.message.reply_text('Hello! This is a custom command?')
    

df = pd.read_csv(r"/Users/martin/Downloads/CAPT/birthdays! - Sheet1.csv")
# value = df.iat[1, 1]


async def continuous_function(update: Update):
    print("teest")
    
    for index, row in df.iterrows():
        # print(row[4], row[5], "!!")
        print('gg')
        if today.strftime('%d/%m') == row.iloc[5]:
            print('gggg')
            return row.iloc[4]


    # Sleep for a period to avoid excessive API calls
    await asyncio.sleep(30)
    
async def happyBirthday(context: CallbackContext):
    print('Happy Birthday')
    await context.bot.send_message(chat_id=update.message.chat.id, text='Happy Birthday ' + df.iat[0,1])

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'who' in processed:
        if (df.iat[0,0] == today.strftime('%d/%m')):
            return  'Happy Birthday ' + df.iat[0,1]
        else:
            return df.iat[0,1]
    
    return 'I do not understand what you wrote'



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text 

    print(f'User ( {update.message.chat.id}) in {message_type} : "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        
        else:
            return
    else:
        print(f'Message type: {message_type}')
        response: str = handle_response(text)
    
    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context : ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()


    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    # app.add_handler(CommandHandler('custom', custom_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    #Polls the bot  
    print('Polling...')
    app.run_polling(poll_interval =3)
    