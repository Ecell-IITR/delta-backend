from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from post.models.post import AbstractPost
from post.utils import unique_slug_generator

COMPETITION_TYPE = (
    (
        'Online', 'Online'
    ),
    (
        'Onspot', 'Onspot'
    )
)


class Competition(AbstractPost):
    """
    This model holds information pertaining to a Competition
    """

    competition_type = models.CharField(
        max_length=255,
        choices=COMPETITION_TYPE,
        default='onspot',
        verbose_name="Competition type"
    )

    bookmarks = models.ManyToManyField(
        to='users.Student',
        related_name='bookmark_competition',
        blank=True
    )

    competition_file = models.FileField(
        verbose_name='Competition file'
    )

    link_to_apply = models.URLField(
        verbose_name='Link to apply fro competition'
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        title = self.title
        user = self.user
        return f'{title} - {user.username}'


@receiver(post_save, sender=Competition)
def create_competition(sender, instance=None, created=False, **kwargs):
    if created or instance.slug is None:
        instance.slug = unique_slug_generator(instance)
        instance.save()
