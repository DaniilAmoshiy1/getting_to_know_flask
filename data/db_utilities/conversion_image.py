"""
This file is for future features
"""
from PIL import Image
import io

from data.daos.dishes_dao import DishesDao

def image_to_bytes(image, dish_id):
    with Image.open(image) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
    dish_update = DishesDao()
    dish_update.update_dish(dish_id=dish_id, photo=img_byte_arr)

# image_bytes = image_to_bytes()


def bytes_to_image(image_bytes):
    img_byte_arr = io.BytesIO(image_bytes)
    img = Image.open(img_byte_arr)
    return img
