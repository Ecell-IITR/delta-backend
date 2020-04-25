from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from post.utils import unique_slug_generator
from utilities.models import TimestampedModel


class AbstractSkill(TimestampedModel):

    slug = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

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


@receiver(post_save, sender=Skill)
def create_project(sender, instance=None, created=False, **kwargs):
    if created or instance.slug is None:
        instance.slug = unique_slug_generator(instance, 'name')
        instance.save()
