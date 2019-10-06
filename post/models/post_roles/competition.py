from django.db import models
from post.models.post import Post

COMPETITION_TYPE = (
    ('online', 'online'),
    ('onspot', 'onspot')
)


class AbstractCompetition(models.Model):
    """
    This model holds information pertaining to a Competition
    """

    post = models.OneToOneField(
        to=Post,
        on_delete=models.CASCADE,
    )

    competition_type = models.CharField(
        max_length=255,
        choices=COMPETITION_TYPE,
        default='onspot',
        verbose_name="Competition type"
    )

    competition_file = models.FileField(
        verbose_name='Competition file'
    )

    link_to_apply = models.URLField(
        verbose_name='Link to apply fro competition'
    )

    class Meta:
        """
        Meta class for AbstractCompetition
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        post = self.post
        return f'{post}'


class Competition(AbstractCompetition):
    """
    This class implements AbstractCompetition
    """

    class Meta:
        """
        Meta class for Competition
        """
        verbose_name_plural = 'Competition'
