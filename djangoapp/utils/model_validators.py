
from django.core.exceptions import ValidationError
from pathlib import Path
from django.conf import settings
from PIL import Image
import string
from random import SystemRandom


def validate_png(image):
    if not image.name.lower().endswith('.png'):
        raise ValidationError('Imagem precisa ser PNG.')




def resize_image(image_django, new_width=800, optimize=True, quality=60):
    image_path = Path(settings.MEDIA_ROOT / image_django.name).resolve()
    image_pillow = Image.open(image_path)
    original_width, original_height = image_pillow.size

    if original_width <= new_width:
        image_pillow.close()
        return image_pillow

    new_height = round(new_width * (original_height / original_width))

    new_image = image_pillow.resize((new_width, new_height), Image.Resampling.LANCZOS)

    new_image.save(
        image_path,
        optimize=optimize,
        quality=quality,
    )

    return new_image




from django.utils.text import slugify


def random_letters(k=5):
    return ''.join(SystemRandom().choices(
        string.ascii_lowercase + string.digits,
        k=k
    ))


def slugify_new(text, k=5):
    return slugify(text) + '-' + random_letters(k)

