import os
import logging
import instaloader
import json
from dotenv import load_dotenv
from telegram import Update, Poll
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Ваши переменные окружения
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
INSTA_USERNAME = 'your_little_toxic_girl_'
INSTA_PASSWORD = '19931204nik'

# Аккаунт, у которого берём сторис
TARGET_USERNAME = "shaurma.na.ugliah"

# Команда /start
async def start():
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await update.message.reply_text("Привет! Отправляю сторис из Instagram...")

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
                        print(photo_path)
                        # with open(photo_path, "rb") as photo:
                            # await update.message.reply_photo(photo)

                        # Создаём опрос
                        # await update.message.reply_poll(
                        #     question="Как тебе шаурма? 🌯",
                        #     options=["Огонь!", "Норм", "Так себе..."],
                        #     is_anonymous=False,
                        #     allows_multiple_answers=False
                        # )
                        return

        # await update.message.reply_text("Нет актуальных сторис 😔")

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        # await update.message.reply_text("Произошла ошибка при получении сторис.")

def get_stories():
    load_dotenv()

    # Создаем экземпляр Instaloader
    L = instaloader.Instaloader()

    try:
        # Авторизация
        print("🔐 Авторизация в Instagram...")
        print("🔐 INSTA_USERNAME", INSTA_USERNAME)
        print("🔐 INSTA_PASSWORD", INSTA_PASSWORD)
        L.login(INSTA_USERNAME, INSTA_PASSWORD)
        print("✅ Успешный вход как", INSTA_USERNAME)

        # Целевой аккаунт
        target_username = "shaurma.na.ugliah"
        profile = instaloader.Profile.from_username(L.context, target_username)

        # Получаем первый (самый свежий) пост
        posts = profile.get_posts()
        first_post = next(posts, None)

        if first_post:
            print("✅ Найден первый пост:")
            print(f"📸 URL изображения: {first_post.url}")
            print(f"📝 Подпись: {first_post.caption}")
        else:
            print("❌ У пользователя нет постов.")

        # print(f"📷 Истории {profile.username}:")
        # stories = L.get_stories(userids=[profile.userid])
        # print(f"📷 stories:", stories)
        #
        # # Если истории найдены, выводим их
        # for story in stories:
        #     print(f"📷 story:", story)
        #     for item in story.get_items():
        #         if item.is_video:
        #             print(f"🎥 Видео URL: {item.video_url}")
        #             print(f"🎥 Видео URL: {item.video_url}")
        #         else:
        #             print(f"🖼 Картинка URL: {item.url}")

    except Exception as e:
        print("❌ Ошибка:", e)

# Запуск бота
# def main():
    # app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    # app.add_handler(CommandHandler("start", start))
    # print("Бот запущен 🚀")
    # app.run_polling()

def main():
    get_stories()

if __name__ == "__main__":
    main()