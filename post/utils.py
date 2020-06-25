import string
import random

from django.utils.text import slugify


def random_string_generator(
    size=10,
    chars=string.ascii_lowercase + string.digits
):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, check_param='title', new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        if check_param == 'title':
            slug = slugify(instance.title)
        elif check_param == 'name':
            slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:

        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )

        return unique_slug_generator(
            instance,
            new_slug=new_slug
        )

    return slug
