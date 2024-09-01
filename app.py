from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler
import os

app = Flask(__name__)

# Функция для инициализации бота
def create_bot(token):
    bot = Bot(token=token)
    dispatcher = Dispatcher(bot, None, workers=0)

    # Команда /start
    def start(update, context):
        keyboard = [
            [InlineKeyboardButton("📊 JetX Progger", url="https://t.me/jetxprogger_bot/JetxPROGGER")],
            [InlineKeyboardButton("🎮 Играем в JetX здесь", url="https://1wxxlb.com/v3/jetx-landing?p=cxp7")],
            [InlineKeyboardButton("📢 Наш Telegram канал", url="https://t.me/+1mHcVfVmYEBmY2Rh")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Добро пожаловать! Выберите один из вариантов:", reply_markup=reply_markup)

    # Обработка нажатий на кнопки
    def button(update, context):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=f"Вы выбрали: {query.data}")

    # Регистрация команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    return bot, dispatcher

# Основная функция приложения
@app.route(f"/<token>", methods=["POST"])
def webhook(token):
    bot, dispatcher = create_bot(token)
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "ok"

if __name__ == "__main__":
    token = input("Введите токен вашего Telegram-бота: ")
    url = input("Введите URL вашего сайта (например, https://your_domain.com): ")

    bot, dispatcher = create_bot(token)
    bot.set_webhook(f"{url}/{token}")

    app.run(host="0.0.0.0", port=5000)
