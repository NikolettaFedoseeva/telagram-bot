import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Команда /start была вызвана.")
    await update.message.reply_photo(
        'https://www.imgonline.com.ua/examples/bee-on-daisy.jpg',
        caption="Привет! Это твоя картинка."
    )

# Функция для обработки команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Команда /help была вызвана.")
    await update.message.reply_text(
        "Этот бот может отправить картинку при команде /start.\n"
        "Просто напишите /start, и я пришлю вам изображение."
    )

def main() -> None:
    # Токен, полученный от @BotFather
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Запуск бота
    print("Бот запущен 🚀")
    application.run_polling()

if __name__ == '__main__':
    main()
