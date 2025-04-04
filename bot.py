import logging
import instaloader
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from instagram_scraper import download_instagram_story

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
USERNAME = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")

# Функция для обработки команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Команда /start была вызвана.")
    await update.message.reply_text("Привет! 👋 Бот работает!")
    # await update.message.reply_photo(
    #     'https://www.imgonline.com.ua/examples/bee-on-daisy.jpg',
    #     caption="Привет! Это твоя картинка."
    # )
# Функция для обработки команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Команда /help была вызвана.")
    await update.message.reply_text(
        "Этот бот может отправить картинку при команде /start.\n"
        "Просто напишите /start, и я пришлю вам изображение."
    )

async def story_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if not context.args:
    #     await update.message.reply_text("❗ Укажи имя пользователя Instagram: /story <username>")
    #     return
    #
    # username = context.args[0]
    await update.message.reply_text(f"🔍 Ищу сторис {INSTAGRAM_USERNAME}...")

    try:
        loader = instaloader.Instaloader(dirname_pattern="stories", download_videos=False, download_video_thumbnails=False)
        loader.login(USERNAME, PASSWORD)
        profile = instaloader.Profile.from_username(loader.context, INSTAGRAM_USERNAME)

        stories = []
        for story in loader.get_stories(userids=[profile.userid]):
            for item in story.get_items():
                loader.download_storyitem(item, target=f"{INSTAGRAM_USERNAME}_story")
                stories.append(item)

        if stories:
            first_item = stories[0]
            for file in os.listdir(f"{INSTAGRAM_USERNAME}_story"):
                if file.endswith(".jpg") and str(first_item.mediaid) in file:
                    with open(os.path.join(f"{INSTAGRAM_USERNAME}_story", file), "rb") as photo:
                        await update.message.reply_photo(photo)
                    break
        else:
            await update.message.reply_text("❌ Нет актуальных сторис.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

def main() -> None:
    # Токен, полученный от @BotFather
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("story", story_command))

    # Запуск бота
    print("Бот запущен 🚀")
    application.run_polling()

if __name__ == '__main__':
    main()
