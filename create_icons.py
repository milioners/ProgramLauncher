from PIL import Image, ImageDraw, ImageFont

# Создаём градиентную иконку
def create_gradient_icon(size=(64, 64), filename="gradient_icon.png"):
    """Создаёт иконку с градиентным фоном."""
    image = Image.new("RGB", size)
    draw = ImageDraw.Draw(image)

    for y in range(size[1]):
        for x in range(size[0]):
            # Градиент от красного к синему
            r = int(255 * (x / size[0]))
            b = int(255 * (y / size[1]))
            draw.point((x, y), fill=(r, 0, b))

    image.save(filename)
    print(f"Создана градиентная иконка: {filename}")


# Создаём иконку с текстом
def create_text_icon(text, size=(64, 64), filename="text_icon.png"):
    """Создаёт иконку с текстом."""
    image = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(image)

    # Используем стандартный шрифт
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Рисуем текст
    draw.text((10, 20), text, fill="black", font=font)

    image.save(filename)
    print(f"Создана текстовая иконка: {filename}")


# Создаём иконку с геометрическими фигурами
def create_shape_icon(size=(64, 64), filename="shape_icon.png"):
    """Создаёт иконку с геометрическими фигурами."""
    image = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(image)

    # Рисуем круг
    draw.ellipse([10, 10, 54, 54], fill="blue", outline="black")

    # Рисуем треугольник
    draw.polygon([32, 10, 10, 54, 54, 54], fill="red", outline="black")

    image.save(filename)
    print(f"Создана иконка с фигурами: {filename}")


# Создаём иконку с прозрачным фоном
def create_transparent_icon(size=(64, 64), filename="transparent_icon.png"):
    """Создаёт иконку с прозрачным фоном."""
    image = Image.new("RGBA", size, (0, 0, 0, 0))  # Прозрачный фон
    draw = ImageDraw.Draw(image)

    # Рисуем звезду
    draw.polygon(
        [(32, 10), (40, 30), (60, 30), (45, 45), (55, 65), (32, 55), (10, 65), (20, 45), (5, 30), (25, 30)],
        fill="yellow", outline="black"
    )

    image.save(filename)
    print(f"Создана прозрачная иконка: {filename}")


# Создаём все иконки
def create_all_icons():
    create_gradient_icon()
    create_text_icon("FAQ")
    create_shape_icon()
    create_transparent_icon()


# Запуск создания иконок
if __name__ == "__main__":
    create_all_icons()