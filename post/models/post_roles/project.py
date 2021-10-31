from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from post.models.applied_post_entries import AppliedPostEntries
from django.contrib.contenttypes.fields import GenericRelation
from post.models.post import AbstractPost
from post.utils import unique_slug_generator
from post.constants import POST_TYPE


class Project(AbstractPost):
    """
    This model holds information pertaining to a Project
    """

    stipend = models.CharField(max_length=55, blank=True, verbose_name="Stipend")

    stipend_max = models.CharField(
        max_length=55, blank=True, null=True, default=None, verbose_name="Stipend Max"
    )

    project_file = models.FileField(verbose_name="Project file", blank=True)

    approx_duration = models.CharField(
        max_length=55, blank=True, verbose_name="Approximate Duration"
    )
    applied_post_entries = GenericRelation(
        AppliedPostEntries,
        content_type_field="post_content_type",
        object_id_field="post_object_id",
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        title = self.title
        user = self.user
        return "%s - %s" % (title, user.username)

    @staticmethod
    def get_post_type():
        return POST_TYPE.PROJECT_POST_TYPE


@receiver(pre_save, sender=Project)
def project_pre_save(instance=None, created=False, update_fields=None, **kwargs):
    project = None
    if not created and update_fields is None:
        try:
            project = Project.objects.get(pk=instance.pk)
        except Project.DoesNotExist:
            pass
    instance.__old_instance = project


@receiver(post_save, sender=Project)
def project_post_save(update_fields, instance=None, created=False, **kwargs):
    if update_fields is None:
        old_inst = instance.__old_instance
        if old_inst is None or old_inst.title != instance.title:
            instance.slug = unique_slug_generator(instance)
            instance.save()
