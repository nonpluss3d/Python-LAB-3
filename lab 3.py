from PIL import Image

#Декодирование
def decode(image_name, key_name):
    img = Image.open(image_name)
    pixels = img.load()

    bits = ""

    with open(key_name, "r") as file:
        for line in file:
            x, y = map(int, line.strip()[1:-1].split(","))

            # Берём зелёный канал
            g = pixels[x, y][1]

            # Получаем 0 бит
            bits += str(g & 1)

    print("Полученные биты:")
    print(bits)

    # Переводим биты в символы
    text = ""

    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]

        if len(byte) == 8:
            text += chr(int(byte, 2))

    print("\nДекодированный текст:")
    print(text)

#Кодирование
def encode(image_name, out_image, text):
    img = Image.open(image_name)
    pixels = img.load()

    # Перевод текста в биты
    bits = ""

    for symbol in text:
        bits += format(ord(symbol), "08b")

    print("Биты первого символа:")
    print(format(ord(text[0]), "08b"))
    print(" ")

    width, height = img.size
    index = 0

    for y in range(height):
        for x in range(width):

            if index >= len(bits):
                break

            r, g, b, a = pixels[x, y]

            old_g = g

            # Меняем 0 бит зелёного канала
            g = (g & ~1) | int(bits[index])

            pixels[x, y] = (r, g, b, a)

            print(f"Пиксель ({x}, {y})")
            print(f"Было: {old_g}")
            print(f"Стало: {g}\n")

            index += 1

        if index >= len(bits):
            break

    img.save(out_image)


# Декодирование
decode("new12.png", "keys12.txt")

# Кодирование
encode("new12.png", "result.png", "RGB")