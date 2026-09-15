import os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


# Render/Linux uses the normal "tesseract" command.
# Windows can use the installed path automatically if it exists.
if os.name == "nt":
    windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(windows_path):
        pytesseract.pytesseract.tesseract_cmd = windows_path


def extract_text(image_path):
    image = Image.open(image_path)

    image = image.convert("L")

    image = image.resize(
        (image.width * 2, image.height * 2)
    )

    image = ImageEnhance.Contrast(image).enhance(2)

    image = image.filter(ImageFilter.SHARPEN)

    text = pytesseract.image_to_string(
        image,
        config="--psm 6"
    )

    return text