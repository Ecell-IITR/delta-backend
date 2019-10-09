from django.db import models

from utilities.models import TimestampedModel


class AbstractSkill(TimestampedModel):

    name = models.CharField(
        max_length=255,
        verbose_name="Skill",
        help_text="Type the skill name you want to add"
    )

    def __str__(self):
        """
       Return the string representation of the model
       :return: the string representation of the model
       """

        name = self.name
        return f'{name}'

    class Meta:
        """
        Meta class for AbstractSkill
        """

        abstract = True


class Skill(AbstractSkill):
    """
    This class implements AbstractSkill
    """

    class Meta:
        """
        Meta class for Skill
        """

        verbose_name_plural = 'Skill'
