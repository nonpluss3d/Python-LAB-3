from PIL import Image

#декодирование
def decode():
    img = Image.open("new12.png")
    pix = img.load()

    #координаты
    f = open("keys12.txt")
    coords = []
    for line in f:
        line = line.strip().strip("()")
        x, y = map(int, line.split(","))
        coords.append((x, y))
    f.close()

    #байты из синего канала
    data = []
    for x, y in coords:
        r, g, b = pix[x, y][:3]
        data.append(b)

    #байты в текст
    text = ""
    for byte in data:
        text += chr(byte)

    print("Сообщение:", text)
    return coords, text


#кодирование
def encode(coords, text):
    img = Image.open("new12.png")
    img = img.convert("RGB")
    pix = img.load()

    #текст в биты
    bits = []
    for c in text:
        byte = ord(c)
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    #первый символ
    if text:
        print("\nПервый символ:", text[0])
        print("Биты:", end=" ")
        for i in range(7, -1, -1):
            print((ord(text[0]) >> i) & 1, end="")
        print()

    #биты в зелёном сигнале
    for i, (x, y) in enumerate(coords):
        if i >= len(bits):
            break
        r, g, b = pix[x, y]

        if i < 8:
            print(f"\nПиксель {i + 1} ({x},{y}):")
            print(f"  Было: G={g}")
            print(f"  Бит: {bits[i]}")

        new_g = g - (g % 2) + bits[i]

        if i < 8:
            print(f"  Стало: G={new_g}")

        pix[x, y] = (r, new_g, b)

    img.save("new_new12.png")


coords, msg = decode()
new_text = input("Введите текст: ")
if not new_text:
    new_text = "Test"
encode(coords, new_text)
