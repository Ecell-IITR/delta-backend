from django.db import models

from post.models.post import AbstractPost


class AbstractProject(AbstractPost):
    """
    This model holds information pertaining to a Project
    """

    stipend = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Stipend'
    )

    project_file = models.FileField(
        verbose_name='Project file'
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

    class Meta:
        """
        Meta class for AbstractProject
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        slug = self.slug
        user = self.user
        return f'{slug} ({user.username})'


class Project(AbstractProject):
    """
    This class implements AbstractProject
    """

    class Meta:
        """
        Meta class for Project
        """
        verbose_name_plural = 'Project'
