#!bin/python3

from PIL import Image

img=Image.open("20131225-IMG_7656.jpg")
width,height=img.size
img.close()
print(width)
print(height)


