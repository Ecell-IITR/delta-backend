from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import models
from post.utils import unique_slug_generator
from utilities.models import TimestampedModel,Skill


class AbstractTypeSkill(TimestampedModel):

    slug = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        db_index=True
    )

    name = models.ForeignKey(Skill, to_field='name', on_delete=models.DO_NOTHING)
    type = models.CharField(
        max_length=255,
        default="tech",
        help_text="Type of skill you want to add"
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


class Type(AbstractTypeSkill):
    """
    This class implements AbstractSkill
    """

    class Meta:
        """
        Meta class for Skill
        """

        verbose_name_plural = 'Type'
