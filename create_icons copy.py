from PIL import Image, ImageDraw, ImageFont

# Создаём иконку для кнопки "Добавить программу"
def create_add_program_icon(size=(64, 64), filename="add_program_icon.png"):
    """Создаёт иконку для кнопки 'Добавить программу'."""
    image = Image.new("RGBA", size, (0, 0, 0, 0))  # Прозрачный фон
    draw = ImageDraw.Draw(image)

    # Рисуем плюс
    draw.rectangle([25, 10, 39, 54], fill="green")  # Вертикальная линия
    draw.rectangle([10, 25, 54, 39], fill="green")  # Горизонтальная линия

    image.save(filename)
    print(f"Создана иконка для 'Добавить программу': {filename}")


# Создаём иконку для кнопки "Настройки"
def create_settings_icon(size=(64, 64), filename="settings_icon.png"):
    """Создаёт иконку для кнопки 'Настройки'."""
    image = Image.new("RGBA", size, (0, 0, 0, 0))  # Прозрачный фон
    draw = ImageDraw.Draw(image)

    # Рисуем шестерёнку
    draw.ellipse([10, 10, 54, 54], outline="blue", width=3)
    for i in range(8):
        angle = i * 45
        draw.line(
            [
                (32 + 20 * (0.8 * (i % 2) + 0.2) * (1 if i < 4 else -1), 32),
                (32 + 30 * (0.8 * (i % 2) + 0.2) * (1 if i < 4 else -1), 32),
            ],
            fill="blue",
            width=3,
        )

    image.save(filename)
    print(f"Создана иконка для 'Настройки': {filename}")


# Создаём иконку для кнопки "Помощь"
def create_help_icon(size=(64, 64), filename="help_icon.png"):
    """Создаёт иконку для кнопки 'Помощь'."""
    image = Image.new("RGBA", size, (0, 0, 0, 0))  # Прозрачный фон
    draw = ImageDraw.Draw(image)

    # Рисуем вопросительный знак
    draw.ellipse([20, 10, 44, 34], outline="orange", width=3)
    draw.line([32, 34, 32, 44], fill="orange", width=3)
    draw.ellipse([30, 48, 34, 52], fill="orange")

    image.save(filename)
    print(f"Создана иконка для 'Помощь': {filename}")


# Создаём иконку для кнопки "Поиск"
def create_search_icon(size=(64, 64), filename="search_icon.png"):
    """Создаёт иконку для кнопки 'Поиск'."""
    image = Image.new("RGBA", size, (0, 0, 0, 0))  # Прозрачный фон
    draw = ImageDraw.Draw(image)

    # Рисуем лупу
    draw.ellipse([10, 10, 44, 44], outline="purple", width=3)
    draw.line([40, 40, 54, 54], fill="purple", width=3)

    image.save(filename)
    print(f"Создана иконка для 'Поиск': {filename}")


# Создаём иконку для кнопки "Создать свою тему"
def create_theme_icon(size=(64, 64), filename="theme_icon.png"):
    """Создаёт иконку для кнопки 'Создать свою тему'."""
    image = Image.new("RGBA", size, (0, 0, 0, 0))  # Прозрачный фон
    draw = ImageDraw.Draw(image)

    # Рисуем палитру
    draw.ellipse([10, 10, 54, 54], outline="red", width=3)
    draw.pieslice([10, 10, 54, 54], start=30, end=90, fill="yellow", outline="black")
    draw.pieslice([10, 10, 54, 54], start=90, end=150, fill="blue", outline="black")
    draw.pieslice([10, 10, 54, 54], start=150, end=210, fill="green", outline="black")

    image.save(filename)
    print(f"Создана иконка для 'Создать свою тему': {filename}")


# Создаём иконку для кнопки "Управление плагинами"
def create_plugins_icon(size=(64, 64), filename="plugins_icon.png"):
    """Создаёт иконку для кнопки 'Управление плагинами'."""
    image = Image.new("RGBA", size, (0, 0, 0, 0))  # Прозрачный фон
    draw = ImageDraw.Draw(image)

    # Рисуем пазл
    draw.rectangle([10, 10, 54, 54], outline="cyan", width=3)
    draw.rectangle([20, 20, 44, 44], outline="cyan", width=3)
    draw.line([20, 32, 44, 32], fill="cyan", width=3)
    draw.line([32, 20, 32, 44], fill="cyan", width=3)

    image.save(filename)
    print(f"Создана иконка для 'Управление плагинами': {filename}")


# Создаём все иконки
def create_all_icons():
    create_add_program_icon()
    create_settings_icon()
    create_help_icon()
    create_search_icon()
    create_theme_icon()
    create_plugins_icon()


# Запуск создания иконок
if __name__ == "__main__":
    create_all_icons()