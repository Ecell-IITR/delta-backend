
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from post.utils import unique_slug_generator
from utilities.models import TimestampedModel, Type


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
    type = models.ForeignKey(Type, to_field='type', on_delete=models.DO_NOTHING)
   
    def __str__(self):
        """
       Return the string representation of the model
       :return: the string representation of the model
       """

        name = self.name
        return '%s' % name

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
    skill = None
    if not created and update_fields is None:
        try:
            skill = Skill.objects.get(pk=instance.pk)
        except Skill.DoesNotExist:
            pass
    instance.__old_instance = skill
@receiver(post_save, sender=Skill)
def skill_post_save(update_fields, instance=None, created=False, **kwargs):
    if update_fields is None:
        old_inst = instance.__old_instance
        if old_inst is None or old_inst.name != instance.name:
            instance.slug = unique_slug_generator(instance, 'name')
            instance.save()