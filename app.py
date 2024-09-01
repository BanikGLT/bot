from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import os

app = Flask(__name__)

# Укажите здесь токен вашего Telegram-бота и URL вашего сайта
TOKEN = "7480718425:AAElZRWRvkRAxSh9ScyK30FNa-IMFGAOmaE"  # Замените на ваш токен
WEBHOOK_URL = "https://banikglt-bot-8d0d.twc1.net"  # Замените на ваш URL

# Функция для инициализации бота
def create_app(token):
    application = Application.builder().token(token).build()

    # Команда /start
    async def start(update: Update, context):
        keyboard = [
            [InlineKeyboardButton("📊 JetX Progger", url="https://t.me/jetxprogger_bot/JetxPROGGER")],
            [InlineKeyboardButton("🎮 Играем в JetX здесь", url="https://1wxxlb.com/v3/jetx-landing?p=cxp7")],
            [InlineKeyboardButton("📢 Наш Telegram канал", url="https://t.me/+1mHcVfVmYEBmY2Rh")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Добро пожаловать! Выберите один из вариантов:", reply_markup=reply_markup)

    # Обработка нажатий на кнопки
    async def button(update: Update, context):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=f"Вы выбрали: {query.data}")

    # Регистрация команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    return application

# Основная функция приложения
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    application = create_app(TOKEN)
    update = Update.de_json(request.get_json(), application.bot)
    application.update_queue.put(update)
    return "ok"

if __name__ == "__main__":
    application = create_app(TOKEN)
    application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

    app.run(host="0.0.0.0", port=8080)
