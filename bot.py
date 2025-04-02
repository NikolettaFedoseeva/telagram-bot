import os
import requests
import schedule
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import datetime

# Токен для бота
BOT_TOKEN = '8086048340:AAG-4pdcyFhWJnlsIkmlHriPfqMRQs9yzck'
INSTAGRAM_USERNAME = 'shaurma.na.ugliah'
auto_mode = True

# Функция для скачивания истории Instagram
def download_instagram_story():
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')  # Укажи путь к chromedriver
    try:
        driver.get(f'https://www.instagram.com/stories/{INSTAGRAM_USERNAME}/')
        time.sleep(5)

        story_image = driver.find_element(By.CSS_SELECTOR, 'img[srcset]')
        image_url = story_image.get_attribute('src')

        image_path = 'story.jpg'
        response = requests.get(image_url)
        with open(image_path, 'wb') as file:
            file.write(response.content)

        return image_path
    except Exception as e:
        print(f"Ошибка при получении истории: {e}")
        return None
    finally:
        driver.quit()

# Функция отправки опроса
def send_poll(update: Update, context: CallbackContext, image_path: str):
    chat_id = update.message.chat_id
    context.bot.send_photo(chat_id=chat_id, photo=open(image_path, 'rb'), caption="Что думаете об этой истории?")
    context.bot.send_poll(chat_id=chat_id, question="Нравится ли вам эта история?", options=["Да", "Нет"])

# Команда /get_story
def get_story(update: Update, context: CallbackContext):
    image_path = download_instagram_story()
    if image_path:
        send_poll(update, context, image_path)
    else:
        update.message.reply_text("Не удалось получить историю 😔")

# Команда /auto_mode для включения/выключения автоматического режима
def auto_mode(update: Update, context: CallbackContext):
    global auto_mode
    auto_mode = not auto_mode
    update.message.reply_text(f"Автоматический режим { 'включен' if auto_mode else 'выключен' }.")

# Автоматическая проверка историй раз в сутки в 07:00 UTC+0
def check_stories():
    if auto_mode:
        image_path = download_instagram_story()
        if image_path:
            # Здесь заменяем chat_id на канал или группу, где нужно публиковать
            # context.bot.send_photo(chat_id='@your_channel', photo=open(image_path, 'rb'), caption="Что думаете об этой истории?")
            # context.bot.send_poll(chat_id='@your_channel', question="Нравится ли вам эта история?", options=["Да", "Нет"])
            print("Отправка истории...")

# Основная функция запуска бота
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("get_story", get_story))
    dispatcher.add_handler(CommandHandler("auto_mode", auto_mode))

    # Запуск бота
    updater.start_polling()

    # Настройка автоматического режима
    schedule.every().day.at("07:00").do(check_stories)

    # Запуск планировщика
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    main()
