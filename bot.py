from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# /start-Befehl
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo! Ich bin dein erster Telegram-Bot 🤖")

# Bot starten
app = ApplicationBuilder().token("8196201379:AAEhgi_oiQBw7kn8hIG1wQKhmoQEMbQicRk").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
