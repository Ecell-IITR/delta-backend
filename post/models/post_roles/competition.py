from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericRelation
from common.field_choices import POST_FIELD_CHOICES
from post.models.applied_post_entries import AppliedPostEntries
from post.models.post import AbstractPost
from post.utils import unique_slug_generator
from post.constants import POST_TYPE


class Competition(AbstractPost):
    """
    This model holds information pertaining to a Competition
    """

    competition_type = models.CharField(
        max_length=255,
        choices=POST_FIELD_CHOICES.COMPETITION_TYPE,
        default='1',
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
        return POST_TYPE.COMPETITION_POST_TYPE


@receiver(pre_save, sender=Competition)
def competition_pre_save(instance=None, created=False, update_fields=None, **kwargs):
    competition = None
    if not created and update_fields is None:
        try:
            competition = Competition.objects.get(pk=instance.pk)
        except Competition.DoesNotExist:
            pass
    instance.__old_instance = competition


@receiver(post_save, sender=Competition)
def competition_post_save(update_fields, instance=None, created=False, **kwargs):
    if update_fields is None:
        old_inst = instance.__old_instance
        if old_inst is None or old_inst.title != instance.title:
            instance.slug = unique_slug_generator(instance)
            instance.save()
