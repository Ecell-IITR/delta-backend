from django.db import models
from utilities.models import TimestampedModel


class AbstractSkillType(TimestampedModel):

    type = models.CharField(
        max_length=255,
        help_text="Type of skill you want to add",
        default=None,
        blank=True,
        null=True
        )

    def __str__(self):
        """
       Return the string representation of the model
       :return: the string representation of the model
       """

        type = self.type
        return '%s' % type

    class Meta:
        """
        Meta class for AbstractSkill
        """

        abstract = True


class SkillType(AbstractSkillType):
    """
    This class implements AbstractSkill
    """

    class Meta:
        """
        Meta class for Skill
        """

        verbose_name_plural = 'Skill Type'
