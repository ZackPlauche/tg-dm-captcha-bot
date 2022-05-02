import random
from pathlib import Path

from captcha.image import ImageCaptcha


def get_name_from_tg_user(user):  # -> str
    name = ""
    name_attrs = ['first_name', 'last_name']
    for attr in name_attrs:
        if hasattr(user, attr):
            if getattr(user, attr):
                name += getattr(user, attr) + " "
    return name.strip()


def get_image_captcha(): # -> tuple[str, str]
    
    # Create images folder if it does not exist
    images_folder = Path('images')
    if not images_folder.exists():
        images_folder.mkdir()

    # Create an image instance of the given size
    image_captcha = ImageCaptcha(width=250, height=90)
    image_captcha_text = str(random.randint(1000, 9999))
    image_captcha.generate(image_captcha_text)

    # Write the image on the given file and save it
    image_captcha_path = str((images_folder / f'{image_captcha_text}.png').absolute())
    image_captcha.write(image_captcha_text, image_captcha_path)

    return (image_captcha_path, image_captcha_text)