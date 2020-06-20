from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from post.utils import unique_slug_generator
from utilities.models import TimestampedModel


class AbstractSkill(TimestampedModel):

    slug = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        db_index=True
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


@receiver(pre_save, sender=Skill)
def skill_pre_save(instance=None, created=False, update_fields=None, **kwargs):
    location = None
    if not created and update_fields is None:
        try:
            location = Skill.objects.get(pk=instance.pk)
        except Skill.DoesNotExist:
            pass
    instance.__old_instance = location


@receiver(post_save, sender=Skill)
def skill_post_save(update_fields, instance=None, created=False, **kwargs):
    if update_fields is None:
        old_inst = instance.__old_instance
        if old_inst is None or old_inst.title != instance.title:
            instance.slug = unique_slug_generator(instance)
            instance.save()
