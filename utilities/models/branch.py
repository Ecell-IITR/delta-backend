from django.db import models

from utilities.models import TimestampedModel


class AbstractBranch(TimestampedModel):

    name = models.CharField(
        max_length=255,
        verbose_name="Branch",
        help_text="Type the branch name to be added.."
    )

    code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Branch Code"
    )

    def __str__(self):
        """
       Return the string representation of the model
       :return: the string representation of the model
       """

        name = self.name
        code = self.code
        return f'{name} - {code}'

    class Meta:
        """
        Meta class for AbstractBranch
        """

        abstract = True


class Branch(AbstractBranch):
    """
    This class implements AbstractBranch
    """

    class Meta:
        """
        Meta class for Branch
        """

        verbose_name_plural = 'Branch'
