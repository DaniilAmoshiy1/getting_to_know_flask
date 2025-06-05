"""
This file is for future features
"""
from PIL import Image
import io

image_path = 'images/1a3c9412b917b5dbf65e03eb7ed4e787.jpg'
def image_to_bytes(image_path):
    with Image.open(image_path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

image_bytes = image_to_bytes(image_path)


def bytes_to_image(image_bytes):
    img_byte_arr = io.BytesIO(image_bytes)
    img = Image.open(img_byte_arr)
    return img
