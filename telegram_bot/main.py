from telegram.ext import MessageHandler, Filters, CommandHandler, Updater
import requests
import logging
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def price(update, context):
    chat_id = update.effective_chat.id
    try:
        res = requests.get(
            f"{os.getenv('SERVICE_URL', 'http://service:8000')}/gdr-wkub")
        price_info = res.json()
        message = f"1 KUB 💰 : ​{price_info['WKUB']} GDR 🐕 \n \n 1 GDR 🐕 : {price_info['GDR']} KUB 💰"
    except Exception:
        message = 'Getting price...📈📈📈🎉🥂🚗💳🤑'
    context.bot.send_message(chat_id=chat_id, text=message)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")

# TODO: Better module init
def main():
    updater = Updater(token=os.getenv("TELEGRAM_TOKEN"), use_context=True)

    dispatcher = updater.dispatcher

    unknown_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(CommandHandler("price", price))
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
