import os
from telegram import Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Функция для команды /start
async def start(update: Update, context):
    print("Вход в функцию start")
    # Отправка картинки по ссылке
    image_url = "https://www.imgonline.com.ua/examples/bee-on-daisy.jpg"
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=image_url, caption="Привет! Вот картинка, как ты и просил!")

# Основная функция для запуска бота
def main():
    print("Вход в функцию main")
    application = Application.builder().token(BOT_TOKEN).build()
    # Обработка команды /start
    application.add_handler(CommandHandler("start", start))

    print("Вход в функцию main application ", application)
    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    print("Бот запущен 🚀")
    main()
