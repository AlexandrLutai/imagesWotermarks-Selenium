import os
from PIL import Image, ImageDraw, ImageFont
from openpyxl import Workbook


class ProcessImage:
    """
    Класс для изменения размера изображений, их оптимизации, добавления водяного знака
    и генерации alt-тегов для SEO.
    """

    def __init__(self, folder_path, target_width=800, quality=85, watermark_text="watermark"):
        """
        Инициализация класса ProcessImage.

        :param folder_path: Путь к папке с изображениями.
        :param target_width: Целевая ширина изображения (по умолчанию 800 пикселей).
        :param quality: Качество изображения после оптимизации (по умолчанию 85).
        :param watermark_text: Текст водяного знака (по умолчанию "watermark").
        """
        self.folder_path = folder_path
        self.target_width = target_width
        self.quality = quality
        self.watermark_text = watermark_text

    def resize_and_optimize_images(self):
        """
        Изменяет размер изображений до заданной ширины, сохраняя пропорции, оптимизирует их,
        добавляет водяной знак и записывает данные в Excel.
        """
        resized_count = 0
        excel_data = []

        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)

            if not os.path.isfile(file_path):
                continue

            try:
                with Image.open(file_path) as img:
                    img = img.convert("RGB")
                    width, height = img.size

                    if width > self.target_width:
                        new_height = int((self.target_width / width) * height)
                        img = img.resize((self.target_width, new_height), Image.ANTIALIAS)

                    img = self._add_watermark(img)
                    img.save(file_path, optimize=True, quality=self.quality)

                    alt_text = self._generate_alt_text(filename)
                    excel_data.append((filename, alt_text))
                    resized_count += 1
            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {e}")

        self._save_to_excel(excel_data)
        print(f"Обработано изображений: {resized_count}")

    def _add_watermark(self, image):
        """
        Добавляет водяной знак на изображение.

        :param image: Объект изображения PIL.
        :return: Изображение с водяным знаком.
        """
        draw = ImageDraw.Draw(image)
        font_size = max(20, image.width // 20)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

     
        text_bbox = draw.textbbox((0, 0), self.watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        
        position = (image.width - text_width - 10, image.height - text_height - 10)

        draw.text(position, self.watermark_text, font=font, fill=(255, 255, 255, 128))
        return image

    def _generate_alt_text(self, filename):
        """
        Генерирует alt-тег для изображения на основе имени файла.

        :param filename: Имя файла изображения.
        :return: Сгенерированный alt-тег.
        """
        base_name = os.path.splitext(filename)[0]
        return f"Изображение товара {base_name.replace('_', ' ').capitalize()}"

    def _save_to_excel(self, data):
        """
        Сохраняет данные об изображениях в Excel-файл.

        :param data: Список кортежей с именами файлов и alt-тегами.
        """
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "SEO Data"

        sheet.append(["Имя файла", "Alt-тег"])

        for filename, alt_text in data:
            sheet.append([filename, alt_text])

        excel_path = os.path.join(self.folder_path, "image_data.xlsx")
        workbook.save(excel_path)
        print(f"Данные сохранены в файл: {excel_path}")


if __name__ == "__main__":
    IMAGE_FOLDER = r"images"  
    processor = ProcessImage(IMAGE_FOLDER, target_width=800, quality=85, watermark_text="watermark")
    processor.resize_and_optimize_images()