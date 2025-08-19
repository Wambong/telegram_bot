import database
from database import print_all_data
import logging
from multiprocessing import Process
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from keyboards import get_professions_keyboard
import profession1
import profession2
import profession3
import profession4

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

AD_IMAGE_URL = 'https://ninjabox.org/storage/daacf755-fec7-4f34-8a76-333f11ac2160/nopmwzpto7xfkvc8.jpg'




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_token = context.bot.token
    logger.info("Command /start received from user %s (%s)", user.id, user.username)
    try:
        # Log user and interaction
        database.log_user(user, bot_token)
        database.log_interaction(user.id, bot_token, 'command', '/start')

        await update.message.reply_photo(
            photo=AD_IMAGE_URL,
            caption="Welcome to Blackshisha! Calculate your profit with our tools!",
            parse_mode='Markdown',
        )
        await update.message.reply_text(
            "Choose your profession:",
            reply_markup=get_professions_keyboard(),
            parse_mode='Markdown',
        )
    except Exception as e:
        logger.error("Error handling /start: %s", e)


async def profession_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = query.from_user
    bot_token = context.bot.token
    await query.answer()
    try:
        # Log interaction
        database.log_interaction(user.id, bot_token, 'profession_selection', data)

        if data == 'prof1_start':
            await profession1.handle_profession1_start(query, context)
        elif data == 'prof2_start':
            await profession2.handle_profession2_start(query, context)
        elif data == 'prof3_start':
            await profession3.handle_profession3_start(query, context)
        elif data == 'prof4_start':
            await profession4.handle_profession4_start(query, context)
        else:
            await query.edit_message_text("Unknown command.")
    except Exception as e:
        logger.error("Error in profession selection: %s", e)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_token = context.bot.token
    logger.info("Message received from user %s (%s): %s", user.id, user.username, update.message.text)
    try:
        # Log interaction
        database.log_interaction(user.id, bot_token, 'message', update.message.text)

        await update.message.reply_text("Please use the buttons below to interact with the bot.")
    except Exception as e:
        logger.error("Error responding to message: %s", e)
def run_bot(token):
    database.init_db()
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(profession_selection, pattern='^prof[1-4]_start$'))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    profession1.setup_handlers(app)
    profession2.setup_handlers(app)
    profession3.setup_handlers(app)
    profession4.setup_handlers(app)
    logger.info("Bot with token %s is running...", token)
    app.run_polling()


if __name__ == '__main__':
    tokens = [
        'TOKEN',
        'TOKEN'

    ]
    print_all_data()
    processes = []
    for token in tokens:
        process = Process(target=run_bot, args=(token,))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
