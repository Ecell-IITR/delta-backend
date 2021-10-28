from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericRelation

from post.models.post import AbstractPost
from post.models.applied_post_entries import AppliedPostEntries
from post.utils import unique_slug_generator
from post.constants import POST_TYPE


class Internship(AbstractPost):
    """
    This model holds information pertaining to a Internship
    """

    stipend = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name='Stipend',
        help_text="Stipend should be in rupees."
    )

    stipend_max = models.CharField(
        max_length=55,
        blank=True,
        null=True,
        default=None,
        verbose_name='Stipend Max'
    )

    position = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Position'
    )

    duration_value = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Duration value in days'
    )

    product_details = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Product Details'
    )

    # work_type = models.PositiveIntegerField(
    #     max_length=255,
    #     blank=True,
    #     choices=POST_FIELD_CHOICES.WORK_TYPE,
    #     default=POST_FIELD_CHOICES.PART_TIME,
    #     verbose_name="Type of Work"
    # )

    applied_post_entries = GenericRelation(AppliedPostEntries, content_type_field='post_content_type',
                                           object_id_field='post_object_id')

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """
        title = self.title
        user = self.user
        return '%s - %s' % (title, user.username)

    @staticmethod
    def get_post_type():
        return POST_TYPE.INTERNSHIP_POST_TYPE


@receiver(pre_save, sender=Internship)
def internship_pre_save(instance=None, created=False, update_fields=None, **kwargs):
    internship = None
    if not created and update_fields is None:
        try:
            internship = Internship.objects.get(pk=instance.pk)
        except Internship.DoesNotExist:
            pass
    instance.__old_instance = internship


@receiver(post_save, sender=Internship)
def internship_post_save(update_fields, instance=None, created=False, **kwargs):
    if update_fields is None:
        old_inst = instance.__old_instance
        if old_inst is None or old_inst.title != instance.title:
            instance.slug = unique_slug_generator(instance)
            instance.save()
