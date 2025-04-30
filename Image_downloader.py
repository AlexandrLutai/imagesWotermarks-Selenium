from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import requests
from PIL import Image
from io import BytesIO


class ImageDownloader:
    """
    Класс для загрузки изображений с Google Images с использованием Selenium.
    """

    def __init__(self, driver_path, download_folder="images"):
        """
        Инициализация класса ImageDownloader.

        :param driver_path: Путь к драйверу Selenium (GeckoDriver).
        :param download_folder: Папка для сохранения загруженных изображений.
        """
        self.driver_path = driver_path
        self.download_folder = download_folder
        os.makedirs(download_folder, exist_ok=True)
        self.driver = None

    def start_driver(self):
        """
        Запускает веб-драйвер Firefox.
        """
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")
        service = Service(self.driver_path)
        self.driver = webdriver.Firefox(service=service, options=options)

    def search_and_download(self, query, max_images=10, min_width=200, min_height=150):
        """
        Выполняет поиск изображений в Google Images и загружает их.

        :param query: Поисковый запрос.
        :param max_images: Максимальное количество изображений для загрузки.
        :param min_width: Минимальная ширина изображения.
        :param min_height: Минимальная высота изображения.
        """
        self.start_driver()
        self._open_google_images()
        self._accept_cookies()
        self._perform_search(query)
        self._scroll_and_collect_images(max_images, min_width, min_height)
        self.driver.quit()

    def _open_google_images(self):
        """
        Открывает страницу Google Images.
        """
        self.driver.get("https://www.google.com/imghp")

    def _accept_cookies(self):
        """
        Принимает куки, если появляется соответствующее окно.
        """
        try:
            accept_cookies_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//div[contains(text(), 'Принять все') or contains(text(), 'Accept all')]]"))
            )
            accept_cookies_button.click()
        except Exception:
            pass

    def _perform_search(self, query):
        """
        Выполняет поиск изображений по заданному запросу.

        :param query: Поисковый запрос.
        """
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

    def _scroll_and_collect_images(self, max_images, min_width, min_height):
        """
        Прокручивает страницу и собирает ссылки на изображения.

        :param max_images: Максимальное количество изображений для загрузки.
        :param min_width: Минимальная ширина изображения.
        :param min_height: Минимальная высота изображения.
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scroll_attempts = 5

        while scroll_attempts < max_scroll_attempts:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            try:
                show_more_button = self.driver.find_element(By.XPATH, "//input[@type='button' and @value='Show more']")
                show_more_button.click()
                time.sleep(2)
            except Exception:
                pass

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
            last_height = new_height

        images = self.driver.find_elements(By.XPATH, "//img[@src or @data-src]")
        self._download_images(images, max_images, min_width, min_height)

    def _download_images(self, images, max_images, min_width, min_height):
        """
        Загружает изображения, соответствующие заданным критериям.

        :param images: Список элементов изображений.
        :param max_images: Максимальное количество изображений для загрузки.
        :param min_width: Минимальная ширина изображения.
        :param min_height: Минимальная высота изображения.
        """
        count = 0
        for img in images:
            if count >= max_images:
                break
            try:
                src = img.get_attribute("src") or img.get_attribute("data-src")
                if src and "http" in src:
                    self._process_image(src, count, min_width, min_height)
                    count += 1
            except Exception:
                pass

    def _process_image(self, src, count, min_width, min_height):
        """
        Обрабатывает изображение: проверяет его размер и сохраняет, если оно соответствует критериям.

        :param src: URL изображения.
        :param count: Текущий номер изображения.
        :param min_width: Минимальная ширина изображения.
        :param min_height: Минимальная высота изображения.
        """
        try:
            response = requests.get(src, stream=True)
            content_type = response.headers.get("Content-Type", "")
            if response.status_code == 200 and "image" in content_type and "svg" not in content_type:
                image = Image.open(BytesIO(response.content))
                if image.width >= min_width and image.height >= min_height:
                    self._save_image(src, f"{self.download_folder}/image_{count}.jpg")
        except Exception:
            pass

    def _save_image(self, url, filepath):
        """
        Сохраняет изображение по указанному URL в файл.

        :param url: URL изображения.
        :param filepath: Путь для сохранения изображения.
        """
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
        except Exception:
            pass


if __name__ == "__main__":
    DRIVER_PATH = r"drivers/geckodriver.exe"
    downloader = ImageDownloader(DRIVER_PATH)
    downloader.search_and_download("Пейзаж", max_images=100)