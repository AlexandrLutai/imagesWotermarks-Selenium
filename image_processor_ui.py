import tkinter as tk
from tkinter import messagebox
from Image_downloader import ImageDownloader
from duplicate_remover import DuplicateRemover
from process_image import ProcessImage


class ImageProcessorApp:
    """
    Приложение с графическим интерфейсом для обработки изображений.
    """

    def __init__(self, root):
        """
        Инициализация приложения.

        :param root: Корневое окно tkinter.
        """
        self.root = root
        self.root.title("Обработка изображений")
        self.root.geometry("400x250")

        # Поле для ввода поискового запроса
        self.query_label = tk.Label(self.root, text="Введите запрос для поиска изображений:", font=("Arial", 10))
        self.query_label.pack(pady=5)

        self.query_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.query_entry.pack(pady=5)

        # Кнопка для запуска обработки изображений
        self.process_button = tk.Button(
            self.root,
            text="Запустить процесс",
            command=self.run_process,
            font=("Arial", 12),
            bg="lightblue",
            fg="black"
        )
        self.process_button.pack(pady=20)

    def run_process(self):
        """
        Запускает процесс: скачивание изображений, удаление дублей, обработка и создание таблицы.
        """
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showerror("Ошибка", "Введите запрос для поиска изображений!")
            return

        try:
            folder_path = "images"  # Папка для сохранения изображений

            # Шаг 1: Скачивание изображений
            downloader = ImageDownloader(driver_path="drivers/geckodriver.exe", download_folder=folder_path)
            downloader.search_and_download(query, max_images=50)
            messagebox.showinfo("Шаг 1", "Скачивание изображений завершено!")

            # Шаг 2: Удаление дублей
            remover = DuplicateRemover(folder_path)
            remover.remove_duplicates()
            messagebox.showinfo("Шаг 2", "Удаление дублей завершено!")

            # Шаг 3: Обработка изображений и создание таблицы
            processor = ProcessImage(folder_path, target_width=800, quality=85, watermark_text="ReCraft")
            processor.resize_and_optimize_images()
            messagebox.showinfo("Шаг 3", "Обработка изображений завершена и таблица создана!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()