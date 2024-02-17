import os
from PIL import Image
import pytesseract
from django.template.context_processors import media
from DPL.settings import MEDIA_ROOT

from django.conf import settings


from ocr_module import *
import cv2

print('ocr')
# To get text from image
print(MEDIA_ROOT)
path2 = os.path.join(MEDIA_ROOT, '2024-02-14/test2.jpg')
print(path2)

