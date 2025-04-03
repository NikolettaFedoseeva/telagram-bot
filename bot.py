import os
import instaloader
import schedule
import time
from telegram import Bot
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")

bot = Bot(token=BOT_TOKEN)


# Функция для скачивания истории
def download_story():
    loader = instaloader.Instaloader(download_pictures=True, quiet=True)
    stories = loader.get_stories()

    for story in stories:
        if story.owner_username.lower() == INSTAGRAM_USERNAME.lower():
            for item in story.get_items():
                loader.download_storyitem(item, "stories")
                file_path = f"stories/{item.mediaid}.jpg"
                return file_path
    return None


# Функция отправки истории в Telegram
def send_story():
    image_path = download_story()
    if image_path:
        bot.send_photo(chat_id="@your_channel", photo=open(image_path, "rb"), caption="Новая история!")
    else:
        bot.send_message(chat_id="@your_channel", text="Историй нет.")


# Автоматический запуск в 07:00 UTC
schedule.every().day.at("07:00").do(send_story)

if __name__ == "__main__":
    print("Бот запущен 🚀")
    while True:
        schedule.run_pending()
        time.sleep(60)
