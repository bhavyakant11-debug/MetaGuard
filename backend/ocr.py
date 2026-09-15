import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image_path):
    """
    Extract text from a product/package image using OCR.
    """

    image = Image.open(image_path)

    # Convert image to grayscale
    image = image.convert("L")

    # Enlarge image for better OCR
    image = image.resize(
        (image.width * 2, image.height * 2)
    )

    # Improve contrast
    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(2)

    # Slightly sharpen the image
    image = image.filter(ImageFilter.SHARPEN)

    # Extract text
    text = pytesseract.image_to_string(
        image,
        config="--psm 6"
    )

    return text