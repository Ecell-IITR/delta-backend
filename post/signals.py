from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from post.models.post import Post


@receiver(pre_save, sender=Post)
def add_slug_to_article_if_not_exists(sender, instance, *args, **kwargs):
    slug = slugify(instance.title) + '-' + instance.id
    instance.slug = slug
