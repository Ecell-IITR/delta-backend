from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.field_choices import POST_FIELD_CHOICES
from post.models.post import AbstractPost
from post.utils import unique_slug_generator


class Internship(AbstractPost):
    """
    This model holds information pertaining to a Internship
    """

    stipend = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Stipend'
    )

    position = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Position'
    )

    duration = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Duration'
    )

    product_details = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Product Details'
    )

    work_type = models.CharField(
        max_length=255,
        choices=POST_FIELD_CHOICES.WORK_TYPE,
        default='part time',
        verbose_name="Type of Work"
    )

    bookmarks = models.ManyToManyField(
        to='users.Student',
        related_name='bookmark_internship',
        blank=True
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """
        title = self.title
        user = self.user
        return f'{title} - {user.username}'


@receiver(post_save, sender=Internship)
def create_internship(sender, instance=None, created=False, **kwargs):
    if created or instance.slug is None:
        instance.slug = unique_slug_generator(instance)
        instance.save()
