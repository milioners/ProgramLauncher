import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json
import os
import requests
from io import BytesIO
import importlib.util
import sys
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk  # Добавляем импорт ttk
import pyperclip 

# Настройка темы и внешнего вида
ctk.set_appearance_mode("System")  # Режим темы: System, Dark, Light
ctk.set_default_color_theme("blue")  # Цветовая тема

# Основной класс программы
class ProgramManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Менеджер программ")
        self.geometry("1200x800")

        # Проверка обновлений при запуске
        self.check_updates_on_startup()

        self.programs = []
        self.plugins = []
        self.plugins_state = {}
        self.settings = {}
        self.load_programs()
        self.settings = self.load_settings()
        self.apply_settings()
        self.load_plugins_state()

        # Загрузка иконок
        self.default_icon = self.load_default_icon()
        self.add_program_icon = self.load_icon("add_program_icon.png")
        self.settings_icon = self.load_icon("settings_icon.png")
        self.help_icon = self.load_icon("help_icon.png")
        self.search_icon = self.load_icon("search_icon.png")
        self.theme_icon = self.load_icon("theme_icon.png")
        self.plugins_icon = self.load_icon("plugins_icon.png")

        # Создаем интерфейс
        self.create_widgets()

        # Загружаем плагины ПОСЛЕ создания интерфейса
        self.load_plugins() 

    def check_for_updates(self):
        """Проверяет наличие обновлений."""
        try:
            # Загружаем информацию о текущей версии
            with open("version.json", "r", encoding="utf-8") as f:
                current_version_info = json.load(f)

            # Загружаем информацию о последней версии с сервера
            response = requests.get("https://example.com/version.json")
            response.raise_for_status()
            latest_version_info = response.json()

            # Сравниваем версии
            if latest_version_info["version"] > current_version_info["version"]:
                return latest_version_info  # Возвращаем информацию о новой версии
            return None  # Обновлений нет
        except Exception as e:
            print(f"Ошибка при проверке обновлений: {e}")
            return None

    def notify_update(self, latest_version_info):
        """Уведомляет пользователя о доступном обновлении."""
        result = messagebox.askyesno(
            "Доступно обновление",
            f"Доступна новая версия {latest_version_info['version']}. Хотите обновить программу?"
        )
        if result:
            self.download_update(latest_version_info["download_url"])

    def download_update(self, download_url):
        """Скачивает и устанавливает обновление."""
        try:
            # Скачиваем обновление
            response = requests.get(download_url)
            response.raise_for_status()

            # Сохраняем обновление во временный файл
            update_file = "update.zip"
            with open(update_file, "wb") as f:
                f.write(response.content)

            # Распаковываем обновление
            with zipfile.ZipFile(update_file, "r") as zip_ref:
                zip_ref.extractall("temp_update")

            # Копируем файлы обновления в папку программы
            for root, dirs, files in os.walk("temp_update"):
                for file in files:
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(".", os.path.relpath(src_path, "temp_update"))
                    shutil.move(src_path, dest_path)

            # Удаляем временные файлы
            shutil.rmtree("temp_update")
            os.remove(update_file)

            # Уведомляем пользователя об успешном обновлении
            messagebox.showinfo("Обновление завершено", "Программа успешно обновлена. Пожалуйста, перезапустите программу.")
        except Exception as e:
            messagebox.showerror("Ошибка обновления", f"Не удалось обновить программу: {e}")


    def load_settings(self):
        """Загружает настройки из файла."""
        default_settings = {
            "theme": "System",
            "color_theme": "blue",
            "language": "ru",
            "programs_folder": "C:/Programs",
            "image_size": [150, 150]  # Новый параметр: размер картинки
        }

        if os.path.exists("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
                user_settings = json.load(f)
                # Объединяем настройки пользователя с настройками по умолчанию
                return {**default_settings, **user_settings}
        return default_settings

    def save_settings(self):
        """Сохраняет настройки в файл."""
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)
        self.apply_settings()  # Применяем настройки
        self.update_ui()  # Обновляем интерфейс

    def apply_settings(self):
        ctk.set_appearance_mode(self.settings["theme"])
        ctk.set_default_color_theme(self.settings["color_theme"])

        if hasattr(self, "program_frame"):
            self.update_ui()

    def open_settings(self):
        """Открывает окно настроек."""
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Настройки")
        settings_window.geometry("400x400")

        # Заголовок
        ctk.CTkLabel(settings_window, text="Настройки", font=("Arial", 16, "bold")).pack(pady=10)

        # Тема
        ctk.CTkLabel(settings_window, text="Тема:").pack(pady=5)
        theme_var = tk.StringVar(value=self.settings["theme"])
        theme_menu = ctk.CTkOptionMenu(
            settings_window,
            values=["System", "Dark", "Light"],
            variable=theme_var
        )
        theme_menu.pack(pady=5)

        # Цветовая тема
        ctk.CTkLabel(settings_window, text="Цветовая тема:").pack(pady=5)
        color_theme_var = tk.StringVar(value=self.settings["color_theme"])
        color_theme_menu = ctk.CTkOptionMenu(
            settings_window,
            values=["blue", "green", "dark-blue"],
            variable=color_theme_var
        )
        color_theme_menu.pack(pady=5)

        

        # Кнопка сохранения
        def save_settings():
            self.settings["theme"] = theme_var.get()
            self.settings["color_theme"] = color_theme_var.get()
            self.save_settings()
            self.apply_settings()
            settings_window.destroy()

        ctk.CTkButton(settings_window, text="Сохранить", command=save_settings).pack(pady=20)

    def update_ui(self):
        """Обновляет интерфейс программы."""
        # Очищаем текущий интерфейс
        for widget in self.winfo_children():
            widget.destroy()

        # Создаем интерфейс заново
        self.create_widgets()

        # Отображаем программы с новыми настройками
        self.display_programs()

    def open_help(self):
        """Открывает окно с помощью по программе."""
        help_window = ctk.CTkToplevel(self)
        help_window.title("Помощь")
        help_window.geometry("1000x600")

        # Основной контейнер
        main_container = ctk.CTkFrame(help_window)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Боковое меню
        sidebar = ctk.CTkFrame(main_container, width=200, corner_radius=10)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        # Основное содержимое
        content_frame = ctk.CTkScrollableFrame(main_container, corner_radius=10)
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Разделы помощи
        help_sections = [
            {
                "title": "Как добавить программу?",
                "content": """
                1. Нажмите кнопку **"Добавить программу"**.
                2. Введите название программы.
                3. Выберите путь к программе.
                4. Нажмите **"Добавить"**.
                """,
                "icon": ""  # Иконка для раздела
            },
            {
                "title": "Как удалить программу?",
                "content": """
                1. Найдите программу в списке.
                2. Нажмите кнопку **"Удалить"** рядом с программой.
                """,
                "icon": ""  # Иконка для раздела
            },
            {
                "title": "Как изменить программу?",
                "content": """
                1. Найдите программу в списке.
                2. Нажмите кнопку **"Изменить"** рядом с программой.
                3. Внесите изменения и нажмите **"Сохранить"**.
                """,
                "icon": ""  # Иконка для раздела
            },
            {
                "title": "Как использовать поиск?",
                "content": """
                1. Введите запрос в поле поиска.
                2. Программы будут отфильтрованы автоматически.
                """,
                "icon": ""  # Иконка для раздела
            },
            {
                "title": "Как добавить картинку?",
                "content": """
                1. Для того что бы добавить картинку вам нужно найти ее в интернете.
                2. Нажмите кнопку "Изменить" рядом с программой.
                3. Найдите строку "Ссылка на изображение" вставить туда ссылку и нажмите "Сохранить".
                4. После чего у вас появиться картинка программы.
                """,
                "icon": ""
            },
            {
                "title": "Как создать плагин?",
                "content": """
                1. Создайте файл плагина:
                - Создайте файл с расширением `.py` в папке `plugins`.
                - Название файла должно быть уникальным (например, `my_plugin.py`).

                2. Скопируйте шаблон плагина:
                - Ниже есть кнопка

                3. Загрузите плагин:
                - Перезапустите программу.
                - Плагин автоматически загрузится, если он включен в настройках.

                4. Управление плагином:
                - Включите или отключите плагин через меню "Плагины".
                - Если плагин добавляет новые элементы в интерфейс, они появятся после его включения.
                """,
                "icon": ""  # Иконка для раздела
            }
        ]

        # Отображение разделов помощи
        for section in help_sections:
            # Карточка раздела
            section_frame = ctk.CTkFrame(content_frame, corner_radius=10)
            section_frame.pack(fill="x", padx=10, pady=5)

            # Заголовок с иконкой
            title_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
            title_frame.pack(fill="x", padx=10, pady=5)

            # Загрузка иконки (если она существует)
            if "icon" in section:
                try:
                    icon = self.load_icon(section["icon"])
                    icon_label = ctk.CTkLabel(title_frame, image=icon, text="")
                    icon_label.image = icon  # Сохраняем ссылку на изображение
                    icon_label.pack(side="left", padx=5)
                except Exception as e:
                    print(f"Ошибка загрузки иконки: {e}")

            # Заголовок раздела
            title_label = ctk.CTkLabel(
                title_frame,
                text=section["title"],
                font=("Arial", 14, "bold")
            )
            title_label.pack(side="left", padx=5)

            # Содержимое раздела (изначально скрыто)
            content_frame_inner = ctk.CTkFrame(section_frame, fg_color="transparent")
            content_label = ctk.CTkLabel(
                content_frame_inner,
                text=section["content"],
                justify="left",
                font=("Arial", 12)
            )
            content_label.pack(anchor="w", padx=10, pady=5)

            # Кнопка для копирования шаблона (только для раздела "Как создать плагин?")
            if section["title"] == "Как создать плагин?":
                def copy_template():
                    template = """
    from base_plugin import BasePlugin
    import customtkinter as ctk

    class MyPlugin(BasePlugin):
        \"\"\"Пример плагина, который добавляет новую кнопку в интерфейс.\"\"\"

        def __init__(self, app):
            super().__init__(app)
            self.description = "Добавляет кнопку 'Мой плагин' в интерфейс."

        def initialize(self):
            \"\"\"Инициализация плагина.\"\"\"
            self.add_button()

        def add_button(self):
            \"\"\"Добавляет кнопку в интерфейс.\"\"\"
            if hasattr(self.app, "sidebar"):  # Проверяем, что sidebar существует
                self.button = ctk.CTkButton(
                    self.app.sidebar,
                    text="Мой плагин",
                    command=self.on_button_click
                )
                self.button.pack(pady=10, padx=10, fill="x")
            else:
                print("Ошибка: sidebar не найден в основном приложении.")

        def on_button_click(self):
            \"\"\"Обработчик нажатия на кнопку.\"\"\"
            print("Плагин 'Мой плагин' был активирован!")

        def remove_elements(self):
            \"\"\"Удаляет кнопку из интерфейса.\"\"\"
            if hasattr(self, "button"):
                self.button.destroy()
                    """
                    pyperclip.copy(template)  # Копируем шаблон в буфер обмена
                    messagebox.showinfo("Успех", "Шаблон плагина скопирован в буфер обмена!")

                copy_button = ctk.CTkButton(
                    content_frame_inner,
                    text="Скопировать шаблон",
                    command=copy_template
                )
                copy_button.pack(pady=10)


            # Кнопка для раскрытия/скрытия
            def toggle_section(frame=content_frame_inner):
                if frame.winfo_ismapped():
                    frame.pack_forget()
                else:
                    frame.pack(fill="x", padx=10, pady=5)

            toggle_button = ctk.CTkButton(
                title_frame,
                text="▼",
                width=30,
                command=toggle_section
            )
            toggle_button.pack(side="right", padx=5)

            # Сохраняем фрейм раздела для навигации
            section["content_frame"] = content_frame_inner

        # Кнопка "Свернуть всё"
        def collapse_all():
            for section in help_sections:
                if "content_frame" in section:
                    section["content_frame"].pack_forget()

        collapse_button = ctk.CTkButton(sidebar, text="Свернуть всё", command=collapse_all)
        collapse_button.pack(pady=10)

        # Кнопки для навигации по разделам
        for section in help_sections:
            button = ctk.CTkButton(
                sidebar,
                text=section["title"],
                command=lambda s=section: s["content_frame"].pack(fill="x", padx=10, pady=5)
            )
            button.pack(pady=5)
        
    def load_icon(self, filename):
        """Загружает иконку из файла."""
        try:
            image = Image.open(filename)
            image = image.resize((20, 20), Image.Resampling.LANCZOS)
            return ctk.CTkImage(image)  # Используем CTkImage
        except Exception as e:
            print(f"Ошибка загрузки иконки {filename}: {e}")
            return None

    def load_default_icon(self):
        """Создает иконку по умолчанию, если файл не найден."""
        try:
            # Создаем пустую иконку
            image = Image.new("RGBA", (20, 20), (0, 0, 0, 0))  # Прозрачная иконка
            return ctk.CTkImage(image)  # Используем CTkImage
        except Exception as e:
            print(f"Ошибка создания иконки по умолчанию: {e}")
            return None
        
    def create_widgets(self):
        # Основной контейнер
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Боковая панель
        self.sidebar = ctk.CTkFrame(main_container, width=200, corner_radius=10)  # Делаем sidebar атрибутом класса
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        # Кнопка "Добавить программу"
        self.add_button = ctk.CTkButton(
            self.sidebar,
            text="Добавить программу",
            image=self.add_program_icon,
            compound="left",
            command=self.add_program
        )
        self.add_button.pack(padx=10, pady=10, fill="x")
        ToolTip(self.add_button, "Добавить новую программу в список")

        self.add_button = ctk.CTkButton(
            self.sidebar,
            text="Настройки",
            image=self.settings_icon,
            compound="left",
            command=self.open_settings
        )
        self.add_button.pack(padx=10, pady=10, fill="x")
        ToolTip(self.add_button, "Открывает меню с настроками")  # Добавляем подсказку

        self.add_button = ctk.CTkButton(
            self.sidebar,
            text="Помощь",
            image=self.help_icon,
            compound="left",
            command=self.open_help
        )
        self.add_button.pack(padx=10, pady=10, fill="x")
        ToolTip(self.add_button, "Открывает меню с Помощью")  # Добавляем подсказку

        ctk.CTkButton(
            self.sidebar,
            text="Плагины",
            image=self.plugins_icon,
            compound="left",
            command=self.open_plugins_manager
        ).pack(pady=10, padx=10, fill="x")

        # Основная область
        content_frame = ctk.CTkFrame(main_container, corner_radius=10)
        content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Верхняя панель с поиском
        top_panel = ctk.CTkFrame(content_frame, height=50, corner_radius=10)
        top_panel.pack(fill="x", padx=10, pady=10)

        self.search_entry = ctk.CTkEntry(
            top_panel,
            placeholder_text="Поиск программ",
            width=400
        )
        self.search_entry.pack(side="left", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", lambda event: self.display_programs())

        # Фрейм для отображения программ
        self.program_frame = ctk.CTkScrollableFrame(content_frame, corner_radius=10)
        self.program_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Отображаем программы
        self.display_programs()

    def on_mousewheel(self, event):
        self.program_frame._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def load_programs(self):
        if os.path.exists("programs.json"):
            with open("programs.json", "r") as f:
                self.programs = json.load(f)
                for program in self.programs:
                    if "image" not in program:
                        program["image"] = ""

    def save_programs(self):
        with open("programs.json", "w") as f:
            json.dump(self.programs, f)

    def add_program(self):
        add_window = ctk.CTkToplevel(self)
        add_window.title("Добавить программу")
        add_window.geometry("400x400")

        ctk.CTkLabel(add_window, text="Название программы:").pack(pady=5)
        name_entry = ctk.CTkEntry(add_window)
        name_entry.pack(pady=5)

        def select_program():
            program_path = filedialog.askopenfilename(
                title="Выберите программу",
                filetypes=(("Исполняемые файлы", "*.exe"), ("Все файлы", "*.*"))
            )
            if program_path:
                path_entry.delete(0, tk.END)
                path_entry.insert(0, program_path)

        ctk.CTkLabel(add_window, text="Путь к программе:").pack(pady=5)
        path_entry = ctk.CTkEntry(add_window)
        path_entry.pack(pady=5)
        ctk.CTkButton(add_window, text="Выбрать", command=select_program).pack(pady=5)

        ctk.CTkLabel(add_window, text="Ссылка на изображение:").pack(pady=5)
        image_entry = ctk.CTkEntry(add_window)
        image_entry.pack(pady=5)

        def save_program():
            name = name_entry.get()
            path = path_entry.get()
            image_url = image_entry.get()

            if name and path:
                self.programs.append({"name": name, "path": path, "image": image_url})
                self.save_programs()
                self.display_programs()
                add_window.destroy()
            else:
                messagebox.showerror("Ошибка", "Заполните название и выберите программу")

        ctk.CTkButton(add_window, text="Добавить", command=save_program).pack(pady=10)

    def display_programs(self):
        """Отображает программы в виде карточек."""
        # Очистка фрейма
        for widget in self.program_frame.winfo_children():
            widget.destroy()

        # Фильтрация программ по поисковому запросу
        search_query = self.search_entry.get().lower()
        filtered_programs = [p for p in self.programs if search_query in p["name"].lower()]

        # Получаем размер картинки из настроек
        image_size = self.settings.get("image_size", [150, 150])  # Используем значение по умолчанию, если ключ отсутствует
        image_width, image_height = image_size

        # Отображение программ в сетке
        for i, program in enumerate(filtered_programs):
            row = i // 3  # 3 колонки
            col = i % 3

            # Создание карточки программы
            program_card = ctk.CTkFrame(self.program_frame, corner_radius=10)
            program_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Изображение программы
            image_frame = ctk.CTkFrame(program_card, corner_radius=10, fg_color="transparent")
            image_frame.pack(pady=10)

            if program.get("image"):
                try:
                    response = requests.get(program["image"])
                    image_data = response.content
                    image = Image.open(BytesIO(image_data))
                    image = image.resize((image_width, image_height), Image.Resampling.LANCZOS)  # Используем новый размер
                    photo = ctk.CTkImage(image)  # Используем CTkImage
                    image_label = ctk.CTkLabel(image_frame, image=photo, text="")
                    image_label.image = photo  # Сохраняем ссылку на изображение
                    image_label.pack()
                except Exception as e:
                    print(f"Ошибка загрузки изображения: {e}")
                    # Используем иконку по умолчанию
                    image_label = ctk.CTkLabel(image_frame, image=self.default_icon, text="")
                    image_label.pack()
            else:
                # Используем иконку по умолчанию
                image_label = ctk.CTkLabel(image_frame, image=self.default_icon, text="")
                image_label.pack()

            # Название программы
            name_label = ctk.CTkLabel(
                program_card,
                text=program["name"],
                font=("Arial", 14, "bold")
            )
            name_label.pack(pady=5)

            # Кнопки управления
            button_frame = ctk.CTkFrame(program_card, fg_color="transparent")
            button_frame.pack(pady=10)

            ctk.CTkButton(
                button_frame,
                text="Запустить",
                width=100,
                command=lambda p=program: self.run_program(p)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                button_frame,
                text="Изменить",
                width=100,
                command=lambda p=program: self.edit_program(p)
            ).pack(side="left", padx=5)

            ctk.CTkButton(
                button_frame,
                text="Удалить",
                width=100,
                command=lambda p=program: self.delete_program(p)
            ).pack(side="left", padx=5)

    def run_program(self, program):
        try:
            os.startfile(program["path"])
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить программу: {e}")

    def edit_program(self, program):
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Изменить программу")
        edit_window.geometry("400x400")

        ctk.CTkLabel(edit_window, text="Название программы:").pack(pady=5)
        name_entry = ctk.CTkEntry(edit_window)
        name_entry.insert(0, program["name"])
        name_entry.pack(pady=5)

        def select_program():
            program_path = filedialog.askopenfilename(
                title="Выберите программу",
                filetypes=(("Исполняемые файлы", "*.exe"), ("Все файлы", "*.*"))
            )
            if program_path:
                path_entry.delete(0, tk.END)
                path_entry.insert(0, program_path)

        ctk.CTkLabel(edit_window, text="Путь к программе:").pack(pady=5)
        path_entry = ctk.CTkEntry(edit_window)
        path_entry.insert(0, program["path"])
        path_entry.pack(pady=5)
        ctk.CTkButton(edit_window, text="Выбрать", command=select_program).pack(pady=5)

        ctk.CTkLabel(edit_window, text="Ссылка на изображение:").pack(pady=5)
        image_entry = ctk.CTkEntry(edit_window)
        image_entry.insert(0, program.get("image", ""))
        image_entry.pack(pady=5)

        def save_changes():
            program["name"] = name_entry.get()
            program["path"] = path_entry.get()
            program["image"] = image_entry.get()
            self.save_programs()
            self.display_programs()
            edit_window.destroy()

        ctk.CTkButton(edit_window, text="Сохранить", command=save_changes).pack(pady=10)

    def delete_program(self, program):
        self.programs.remove(program)
        self.save_programs()
        self.display_programs()

    def add_button(self, text, command):
        button = ctk.CTkButton(self, text=text, command=command)
        return button

    def load_plugins_state(self):
        """Загружает состояние плагинов из файла."""
        if os.path.exists("plugins_state.json"):
            with open("plugins_state.json", "r") as f:
                self.plugins_state = json.load(f)
        else:
            self.plugins_state = {}

    def save_plugins_state(self):
        """Сохраняет состояние плагинов в файл."""
        with open("plugins_state.json", "w") as f:
            json.dump(self.plugins_state, f, indent=4)

    def load_plugins(self):
        """Загружает плагины из папки plugins."""
        plugins_dir = "plugins"
        if not os.path.exists(plugins_dir):
            os.makedirs(plugins_dir)  # Создаем папку, если она не существует

        # Добавляем папку plugins в sys.path
        if plugins_dir not in sys.path:
            sys.path.append(plugins_dir)

        self.load_plugins_state()  # Загружаем состояние плагинов

        print("Начало загрузки плагинов...")
        for filename in os.listdir(plugins_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                plugin_path = os.path.join(plugins_dir, filename)
                try:
                    # Динамически загружаем плагин
                    spec = importlib.util.spec_from_file_location("plugin", plugin_path)
                    plugin = importlib.util.module_from_spec(spec)
                    sys.modules["plugin"] = plugin
                    spec.loader.exec_module(plugin)

                    # Инициализируем плагин, если он включен
                    if hasattr(plugin, "ExamplePlugin"):  # Проверяем наличие класса ExamplePlugin
                        plugin_name = filename[:-3]  # Убираем расширение .py
                        if self.plugins_state.get(plugin_name, True):  # По умолчанию включен
                            plugin_instance = plugin.ExamplePlugin(self)  # Передаем self в плагин
                            plugin_instance.initialize()
                            self.plugins.append(plugin_instance)
                            print(f"Плагин '{filename}' успешно загружен.")
                except Exception as e:
                    print(f"Ошибка загрузки плагина '{filename}': {e}")
        print("Загрузка плагинов завершена.")

    def toggle_plugin(self, plugin_name, enabled):
        """Включает или отключает плагин."""
        # Сохраняем состояние плагина
        self.plugins_state[plugin_name] = enabled
        self.save_plugins_state()

        # Перезагружаем плагины
        self.reload_plugins()

    def reload_plugins(self):
        """Перезагружает плагины."""
        # Удаляем все элементы, добавленные плагинами
        for plugin in self.plugins:
            if hasattr(plugin, "remove_elements"):
                plugin.remove_elements()

        # Очищаем список плагинов
        self.plugins = []

        # Загружаем плагины заново
        self.load_plugins()

        # Обновляем интерфейс
        self.update_ui()

    def open_plugins_manager(self):
        """Открывает окно для управления плагинами."""
        plugins_window = ctk.CTkToplevel(self)
        plugins_window.title("Управление плагинами")
        plugins_window.geometry("400x300")

        # Заголовок
        ctk.CTkLabel(plugins_window, text="Плагины", font=("Arial", 16, "bold")).pack(pady=10)

        # Фрейм для списка плагинов
        plugins_frame = ctk.CTkScrollableFrame(plugins_window)
        plugins_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Отображение списка плагинов
        for plugin in self.plugins:
            plugin_name = plugin.__class__.__name__  # Получаем имя класса плагина
            plugin_state = self.plugins_state.get(plugin_name, True)  # По умолчанию включен

            # Фрейм для плагина
            plugin_frame = ctk.CTkFrame(plugins_frame)
            plugin_frame.pack(fill="x", padx=5, pady=5)

            # Чекбокс для включения/отключения плагина
            var = tk.BooleanVar(value=plugin_state)
            checkbox = ctk.CTkCheckBox(plugin_frame, text=plugin_name, variable=var)
            checkbox.pack(side="left", padx=5, pady=5)

            # Описание плагина
            if hasattr(plugin, "description"):
                description_label = ctk.CTkLabel(
                    plugin_frame,
                    text=plugin.description,
                    font=("Arial", 12),
                    wraplength=300,  # Ограничиваем ширину текста
                    justify="left"
                )
                description_label.pack(side="left", padx=5, pady=5)

            # Сохранение состояния при изменении
            checkbox.configure(command=lambda p=plugin_name, v=var: self.toggle_plugin(p, v.get()))

class ToolTip:
    def __init__(self, widget, text):
        """
        Инициализация всплывающей подсказки.

        :param widget: Виджет, к которому привязывается подсказка.
        :param text: Текст подсказки.
        """
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)  # Привязка к событию наведения
        self.widget.bind("<Leave>", self.hide_tooltip)  # Привязка к событию ухода

    def show_tooltip(self, event):
        """Показывает всплывающую подсказку."""
        x, y, _, _ = self.widget.bbox("insert")  # Получаем координаты виджета
        x += self.widget.winfo_rootx() + 25  # Смещаем подсказку относительно виджета
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)  # Создаем новое окно для подсказки
        self.tooltip.wm_overrideredirect(True)  # Убираем рамку и заголовок окна
        self.tooltip.wm_geometry(f"+{x}+{y}")  # Устанавливаем позицию окна

        label = ttk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        """Скрывает всплывающую подсказку."""
        if self.tooltip:
            self.tooltip.destroy()  # Уничтожаем окно подсказки
            self.tooltip = None
            
if __name__ == "__main__":
    app = ProgramManager()
    app.mainloop()