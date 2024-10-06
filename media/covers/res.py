from PIL import Image
import os
for i in os.listdir():
    if i == "res.py":
        continue
    image_path = i

    img = Image.open(image_path)
    # изменяем размер
    new_image = img.resize((380, 562))
    # сохранение картинки
    new_image.save(i)