import os
import logging
import instaloader
from telegram import Update, Poll
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Ваши переменные окружения
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
INSTA_USERNAME = os.getenv("LOGIN")
INSTA_PASSWORD = os.getenv("PASSWORD")

# Аккаунт, у которого берём сторис
TARGET_USERNAME = "shaurma.na.ugliah"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправляю сторис из Instagram...")

    # Авторизация в Instagram
    loader = instaloader.Instaloader(download_videos=False, download_video_thumbnails=False)
    try:
        loader.login(INSTA_USERNAME, INSTA_PASSWORD)
        profile = instaloader.Profile.from_username(loader.context, TARGET_USERNAME)
        logging.info(f"Получен профиль: {profile.username}")

        for story in loader.get_stories(userids=[profile.userid]):
            for item in story.get_items():
                # Сохраняем изображение
                loader.download_storyitem(item, TARGET_USERNAME)
                for file in os.listdir(TARGET_USERNAME):
                    if file.endswith(".jpg") and str(item.mediaid) in file:
                        photo_path = os.path.join(TARGET_USERNAME, file)
                        with open(photo_path, "rb") as photo:
                            await update.message.reply_photo(photo)

                        # Создаём опрос
                        await update.message.reply_poll(
                            question="Как тебе шаурма? 🌯",
                            options=["Огонь!", "Норм", "Так себе..."],
                            is_anonymous=False,
                            allows_multiple_answers=False
                        )
                        return

        await update.message.reply_text("Нет актуальных сторис 😔")

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text("Произошла ошибка при получении сторис.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Бот запущен 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
