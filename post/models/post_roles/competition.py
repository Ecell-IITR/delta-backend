from django.db import models

from post.models.post import AbstractPost

COMPETITION_TYPE = (
    (
        'Online', 'Online'
    ),
    (
        'Onspot', 'Onspot'
    )
)


class AbstractCompetition(AbstractPost):
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

        slug = self.slug
        user = self.user
        return f'{slug} ({user.username})'


class Competition(AbstractCompetition):
    """
    This class implements AbstractCompetition
    """

    class Meta:
        """
        Meta class for Competition
        """
        verbose_name_plural = 'Competition'
