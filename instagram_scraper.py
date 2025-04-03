import instaloader
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")


def download_instagram_story():
    """Скачивает последнюю историю Instagram для указанного профиля"""
    loader = instaloader.Instaloader(download_pictures=True, download_videos=False)

    try:
        # Скачиваем истории
        loader.download_profile(INSTAGRAM_USERNAME, profile_pic=False, fast_update=True, stories=True)

        # Находим последнюю скачанную историю
        profile_folder = f"./{INSTAGRAM_USERNAME}"
        if not os.path.exists(profile_folder):
            print("⚠️ Истории не найдены!")
            return None

        story_files = sorted(
            [os.path.join(profile_folder, f) for f in os.listdir(profile_folder) if f.endswith(".jpg")],
            key=os.path.getmtime,
            reverse=True
        )

        if not story_files:
            print("⚠️ Нет доступных историй.")
            return None

        latest_story = story_files[0]
        print(f"✅ История скачана: {latest_story}")
        return latest_story

    except Exception as e:
        print(f"❌ Ошибка при скачивании истории: {e}")
        return None
