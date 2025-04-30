import os
from PIL import Image
import hashlib


class DuplicateRemover:
    """
    Класс для работы с изображениями, включая удаление дубликатов.
    """

    def __init__(self, folder_path):
        """
        Инициализация класса ImageProcessor.

        :param folder_path: Путь к папке с изображениями.
        """
        self.folder_path = folder_path

    def remove_duplicates(self):
        """
        Удаляет дубликаты изображений в указанной папке.
        Дубликаты определяются по хэшу содержимого изображения.
        """
        hashes = {}
        duplicates = 0

        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)

            if not os.path.isfile(file_path):
                continue

            try:
                with Image.open(file_path) as img:
                    img_hash = self._get_image_hash(img)

                if img_hash in hashes:
                    os.remove(file_path)
                    duplicates += 1
                else:
                    hashes[img_hash] = file_path
            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {e}")

        print(f"Удалено дубликатов: {duplicates}")

    def _get_image_hash(self, image):
        """
        Вычисляет хэш изображения.

        :param image: Объект изображения PIL.
        :return: Хэш изображения.
        """
        hasher = hashlib.md5()
        hasher.update(image.tobytes())
        return hasher.hexdigest()


if __name__ == "__main__":
    IMAGE_FOLDER = r"images"  # Укажите путь к папке с изображениями
    processor = DuplicateRemover(IMAGE_FOLDER)
    processor.remove_duplicates()