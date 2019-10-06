from django.db import models
from post.models.post import Post
from users.models.person import Person


class AbstractProject(models.Model):
    """
    This model holds information pertaining to a Project
    """
    post = models.OneToOneField(
        to=Post,
        on_delete=models.CASCADE,
    )

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

        post = self.post
        return f'{post}'


class Project(AbstractProject):
    """
    This class implements AbstractProject
    """

    class Meta:
        """
        Meta class for Project
        """
        verbose_name_plural = 'Project'
