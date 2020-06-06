from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericRelation

from utilities.models import Tag

from common.field_choices import POST_FIELD_CHOICES

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
        verbose_name='Stipend',
        help_text="Stipend should be in rupees."
    )

    position = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Position'
    )

    duration_value = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Duration'
    )

    duration_unit = models.PositiveIntegerField(
        blank=True,
        choices=POST_FIELD_CHOICES.DURATION_UNIT,
        default=POST_FIELD_CHOICES.MONTH
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

    bookmarks = models.ManyToManyField(
        to='users.Student',
        related_name='bookmark_internship',
        blank=True
    )

    tags = models.ManyToManyField(Tag, related_name='internship_tags', blank=True)

    applied_post_entries = GenericRelation(AppliedPostEntries, content_type_field='post_content_type',
                                                    object_id_field='post_object_id')

    required_skills = models.ManyToManyField(
        to='utilities.Skill',
        related_name='required_skills_internships',
        blank=True,
        verbose_name='Required skill set'
    )

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """
        title = self.title
        user = self.user
        return f'{title} - {user.username}'

    @staticmethod
    def get_post_type():
        return POST_TYPE.INTERNSHIP_POST_TYPE


@receiver(post_save, sender=Internship)
def create_internship(sender, instance=None, created=False, **kwargs):
    if created or instance.slug is None:
        instance.slug = unique_slug_generator(instance)
        instance.save()
