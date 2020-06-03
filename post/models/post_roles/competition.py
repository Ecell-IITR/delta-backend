from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from utilities.models import Tag
from common.field_choices import POST_FIELD_CHOICES
from post.models.post import AbstractPost
from post.utils import unique_slug_generator


class Competition(AbstractPost):
    """
    This model holds information pertaining to a Competition
    """

    competition_type = models.CharField(
        max_length=255,
        choices=POST_FIELD_CHOICES.COMPETITION_TYPE,
        default=POST_FIELD_CHOICES.ONLINE,
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

    tags = models.ManyToManyField(Tag, related_name='competition_tags', blank=True)

    required_skills = models.ManyToManyField(
        to='utilities.Skill',
        related_name='required_skills_competitions',
        blank=True,
        verbose_name='Required skill set'
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
