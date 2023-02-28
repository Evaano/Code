import sys
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'

if len(sys.argv) != 2:
    print("Usage: python script.py image_file")
    sys.exit(1)

filename = sys.argv[1]
try:
    image = Image.open(filename)
except IOError:
    print("Could not open the image file")
    sys.exit(1)

image = Image.open(filename)
ocr_result = pytesseract.image_to_string(image)
ocr_list = ocr_result.split()

for char in ocr_list:
    if char.startswith('BLAZ'):
        print(char)

print(ocr_list[7])
image.show()