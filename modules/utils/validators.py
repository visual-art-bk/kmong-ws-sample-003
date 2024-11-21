from PIL import Image
from io import BytesIO

def is_valid_image(img_content):
    try:
        img = Image.open(BytesIO(img_content))
        img.verify()
        if img.height < 200:
            return False
        return True
    except (IOError, SyntaxError):
        return False