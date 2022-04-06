import random
from pathlib import Path

from captcha.image import ImageCaptcha


def get_captcha():
    images_folder = Path('images')
    
    # Create images folder if it does not exist
    if not images_folder.exists():
        images_folder.mkdir()

    # Create an image instance of the given size
    image = ImageCaptcha(width=250, height=90)
    image_captcha_text = str(random.randint(1000, 9999))
    image.generate(image_captcha_text)

    # Write the image on the given file and save it
    captcha_image_path = str(images_folder / f'{image_captcha_text}.png')
    image.write(image_captcha_text, captcha_image_path)

    return (captcha_image_path, image_captcha_text)