import customtkinter as ctk
import tkinter as tk

class BasePlugin:
    """Базовый класс для всех плагинов"""
    def __init__(self, app):
        self.app = app  # Ссылка на главное приложение
        self.name = "Базовый плагин"
        self.description = "Описание плагина"
        self.version = "1.0"
        self.elements = []  # Для хранения всех созданных элементов
        
    def initialize(self):
        """Инициализация плагина"""
        pass
        
    def remove_elements(self):
        """Удаление всех элементов плагина"""
        for element in self.elements[:]:  # Используем копию списка для безопасного удаления
            try:
                if isinstance(element, str):
                    # Для пунктов меню
                    if hasattr(self.app, 'sidebar_menu'):
                        self.app.sidebar_menu.delete(element)
                elif hasattr(element, 'destroy'):
                    # Для виджетов
                    element.destroy()
            except Exception as e:
                print(f"Ошибка при удалении элемента плагина: {e}")
            finally:
                if element in self.elements:
                    self.elements.remove(element)