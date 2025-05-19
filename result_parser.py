import logging
import asyncio
import nest_asyncio
from flask import Flask, request
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    Application,
    ContextTypes,
)
from telegram import Update
from solana_functions import (
    setup_database,
    add_wallet_to_db,
    get_wallets_from_db,
    filter_transactions,
)
from settings import TELEGRAM_BOT_KEY, BOT_TOKEN

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

flask_app = Flask(__name__)
app = None  # Telegram Application instance


@flask_app.route(f"/{BOT_TOKEN}", methods=["POST"])
def receive_update():
    json_update = request.get_json()
    update = Update.de_json(json_update, app.bot)
    asyncio.create_task(app.update_queue.put(update))
    return "", 200


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🐋 Welcome to the Solana Whale Tracker Bot!")


async def add_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        address, nickname = context.args[0], " ".join(context.args[1:])
        add_wallet_to_db(address, nickname)
        await update.message.reply_text(f"✅ Added: {nickname} - {address}")
    except Exception:
        await update.message.reply_text("Usage: /add_wallet <address> <nickname>")


async def list_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallets = get_wallets_from_db()
    if not wallets:
        await update.message.reply_text("No wallets are currently being tracked.")
        return
    message = "Tracked Wallets:\n" + "\n".join([f"{nick} - {addr}" for addr, nick in wallets])
    await update.message.reply_text(message)


async def track_wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallets = get_wallets_from_db()
    for address, nickname in wallets:
        await filter_transactions(address, nickname, context)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text(f"You said: {update.message.text}")


async def main():
    global app
    setup_database()

    app = Application.builder().token(TELEGRAM_BOT_KEY).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_wallet", add_wallet))
    app.add_handler(CommandHandler("list_wallets", list_wallets))
    app.add_handler(CommandHandler("track_wallets", track_wallets))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("Bot started - using polling (no webhook)")
    await app.run_polling()


if name == "__main__":
    nest_asyncio.apply()  # Useful if running inside Jupyter or Flask dev server

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot stopped by user")