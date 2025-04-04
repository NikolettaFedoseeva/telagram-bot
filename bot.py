import logging
import instaloader
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import subprocess
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
    print("Привет! 👋 Бот работает!")
    # await update.message.reply_text("Привет! 👋 Бот работает!")
    # await update.message.reply_photo(
    #     'https://www.imgonline.com.ua/examples/bee-on-daisy.jpg',
    #     caption="Привет! Это твоя картинка."
    # )
# Функция для обработки команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Команда /help была вызвана.")
    print(
        "Этот бот может отправить картинку при команде /start.\n"
        "Просто напишите /start, и я пришлю вам изображение."
    )
    # await update.message.reply_text(
    #     "Этот бот может отправить картинку при команде /start.\n"
    #     "Просто напишите /start, и я пришлю вам изображение."
    # )


async def story_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"🔍 Ищу сторис {INSTAGRAM_USERNAME}...")

    try:
        loader = instaloader.Instaloader(dirname_pattern="stories", download_videos=False,
                                         download_video_thumbnails=False)

        # Авторизация
        loader.login(USERNAME, PASSWORD)

        # Получение профиля
        profile = instaloader.Profile.from_username(loader.context, INSTAGRAM_USERNAME)
        print('Получен профиль', profile.username)

        # Получение сторис
        stories = []
        print(f"Загружаю сторис для {INSTAGRAM_USERNAME}")
        for story in loader.get_stories(userids=[profile.userid]):
            if not isinstance(story, instaloader.Story):
                print(f"❌ Ошибка при получении сторис для {INSTAGRAM_USERNAME}.")
                continue

            if not story.get_items():
                print(f"❌ Нет актуальных сторис для {INSTAGRAM_USERNAME}.")
                continue

            for item in story.get_items():
                loader.download_storyitem(item, target=f"{INSTAGRAM_USERNAME}_story")
                stories.append(item)

        if stories:
            first_item = stories[0]
            for file in os.listdir(f"{INSTAGRAM_USERNAME}_story"):
                if file.endswith(".jpg") and str(first_item.mediaid) in file:
                    with open(os.path.join(f"{INSTAGRAM_USERNAME}_story", file), "rb") as photo:
                        print(f'Найдено фото: {file}')
                        # await update.message.reply_photo(photo)
                    break
        else:
            print("❌ Нет актуальных сторис.")
            # await update.message.reply_text("❌ Нет актуальных сторис.")
    except instaloader.exceptions.BadCredentialsException:
        print("⚠️ Ошибка: Неверные данные для входа в Instagram.")
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"⚠️ Ошибка: Профиль {INSTAGRAM_USERNAME} не существует.")
    except Exception as e:
        print(f"⚠️ Ошибка: {str(e)}")


def download_stories_cli(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        subprocess.run([
            'instaloader',
            '--login', INSTAGRAM_USERNAME,
            '--stories-only',
            f':stories {INSTAGRAM_USERNAME}'
        ], check=True)
        print("✅ Сторис загружены через CLI")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при загрузке сторис через CLI: {e}")

async def story_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # if not context.args:
    #     await update.message.reply_text("❗ Укажи имя пользователя Instagram: /story <username>")
    #     return
    #
    # username = context.args[0]
    print(f"🔍 Ищу сторис {INSTAGRAM_USERNAME}...")
    # await update.message.reply_text(f"🔍 Ищу сторис {INSTAGRAM_USERNAME}...")

    try:
        loader = instaloader.Instaloader(dirname_pattern="stories", download_videos=False, download_video_thumbnails=False)
        loader.login(USERNAME, PASSWORD)
        # Получение профиля
        profile = instaloader.Profile.from_username(loader.context, INSTAGRAM_USERNAME)
        print('Получен профиль', profile.username)

        # Получение сторис
        stories = []
        print(f"Загружаю сторис для {INSTAGRAM_USERNAME}")
        for story in loader.get_stories(userids=[profile.userid]):
            if not story.get_items():
                print("❌ Нет сторис.")
            else:
                for item in story.get_items():
                    loader.download_storyitem(item, target=f"{INSTAGRAM_USERNAME}_story")
                    stories.append(item)

        if stories:
            first_item = stories[0]
            for file in os.listdir(f"{INSTAGRAM_USERNAME}_story"):
                if file.endswith(".jpg") and str(first_item.mediaid) in file:
                    with open(os.path.join(f"{INSTAGRAM_USERNAME}_story", file), "rb") as photo:
                        print(f'Найдено фото: {file}')
                        # await update.message.reply_photo(photo)
                    break
        else:
            print("❌ Нет актуальных сторис.")
            # await update.message.reply_text("❌ Нет актуальных сторис.")
    except instaloader.exceptions.BadCredentialsException:
        print("⚠️ Ошибка: Неверные данные для входа в Instagram.")
        # await update.message.reply_text("⚠️ Ошибка: Неверные данные для входа в Instagram.")
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"⚠️ Ошибка: Профиль {INSTAGRAM_USERNAME} не существует.")
        # await update.message.reply_text(f"⚠️ Ошибка: Профиль {INSTAGRAM_USERNAME} не существует.")
    except Exception as e:
        print(f"⚠️ Ошибка: {str(e)}")
        # await update.message.reply_text(f"⚠️ Ошибка: {str(e)}")

def main() -> None:
    # Токен, полученный от @BotFather
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("story", story_command))
    application.add_handler(CommandHandler("download_stories_cli", download_stories_cli))

    # Запуск бота
    print("Бот запущен 🚀")
    application.run_polling()

if __name__ == '__main__':
    main()
