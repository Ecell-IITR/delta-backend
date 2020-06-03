from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from utilities.models import Tag
from post.models.post import AbstractPost
from post.utils import unique_slug_generator


class Project(AbstractPost):
    """
    This model holds information pertaining to a Project
    """

    stipend = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Stipend'
    )

    project_file = models.FileField(
        verbose_name='Project file',
        blank=True
    )

    approx_duration = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Approximate Duration'
    )

    bookmarks = models.ManyToManyField(
        to='users.Student',
        related_name='bookmark_project',
        blank=True
    )

    tags = models.ManyToManyField(Tag, related_name='project_tags', blank=True)

    required_skills = models.ManyToManyField(
        to='utilities.Skill',
        related_name='required_skills_project',
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


@receiver(post_save, sender=Project)
def create_project(sender, instance=None, created=False, **kwargs):
    if created or instance.slug is None:
        instance.slug = unique_slug_generator(instance)
        instance.save()
