import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

USERNAME = "shaurma.na.ugliah"
COOKIES_FILE = "cookies.json"

def load_cookies(driver, cookies_path):
    with open(cookies_path, 'r') as f:
        cookies = json.load(f)
    for cookie in cookies:
        if 'sameSite' in cookie:
            if cookie['sameSite'] == 'None':
                cookie['sameSite'] = 'Strict'
        driver.add_cookie(cookie)

def get_story():
    print("🚀 Запуск браузера...")
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    driver = uc.Chrome(options=options)

    try:
        driver.get("https://www.instagram.com/")
        time.sleep(5)

        print("🍪 Добавление cookies...")
        load_cookies(driver, COOKIES_FILE)
        driver.get(f"https://www.instagram.com/{USERNAME}/")
        time.sleep(5)

        print(f"🔍 Переход на профиль {USERNAME}")
        story_ring = driver.find_element(By.CSS_SELECTOR, "canvas")  # Истории подсвечиваются кольцом
        story_ring.click()
        time.sleep(5)

        print("📷 Сохраняем URL изображения истории...")
        img = driver.find_element(By.CSS_SELECTOR, "img[decoding='auto']")
        img_url = img.get_attribute("src")

        print("✅ История найдена:", img_url)

        # Сохраняем картинку
        import requests
        response = requests.get(img_url)
        with open("story.jpg", "wb") as f:
            f.write(response.content)

        print("💾 Картинка сохранена как story.jpg")

    except Exception as e:
        print("❌ Ошибка:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    get_story()
