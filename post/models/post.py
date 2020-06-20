import datetime

from ckeditor_uploader.fields import RichTextUploadingField

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from utilities.models import TimestampedModel, Location, Tag
from users.models.person import Person


class AbstractPost(TimestampedModel):
    """
    This model describes a Post who uses Delta
    """

    slug = models.SlugField(
        db_index=True,
        max_length=255,
        null=True,
        blank=True
    )

    user = models.ForeignKey(
        Person,
        related_name='%(app_label)s_%(class)s',
        on_delete=models.CASCADE
    )

    title = models.CharField(
        default="title",
        max_length=100,
        verbose_name="Title"
    )

    description = RichTextUploadingField(
        blank=True,
        null=True
    )

    post_expiry_date = models.DateTimeField(
        blank=True,
        verbose_name="Post expiry date"
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name="Published"
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name="Verified"
    )

    location = models.ForeignKey(
        to=Location,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    bookmarks = models.ManyToManyField(
        to='users.Student',
        related_name='%(app_label)s_%(class)s_bookmarks',
        blank=True
    )

    tags = models.ManyToManyField(Tag, related_name='%(app_label)s_%(class)s_tags', blank=True)

    required_skills = models.ManyToManyField(
        to='utilities.Skill',
        related_name='%(app_label)s_%(class)s_required_skills',
        blank=True,
        verbose_name='Required skill set'
    )

    start_timestamp = models.DateTimeField(
        auto_now=True
    )

    @property
    def is_expired(self):
        """
        Return whether post has expired or not
        True /False 
        """
        return datetime.date.today() > self.post_expiry_date

    class Meta:
        """
        Meta class for AbstractPost
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        return self.user

    def clean(self, *args, **kwargs):
        errors = {}
        now = timezone.now()
        if hasattr(self, 'post_expiry_date') and self.post_expiry_date:
            if self.post_expiry_date < now:
                errors.setdefault('post_expiry_date', []).append(
                    'Post expiry date cannot be less than current time.')

        if len(errors) > 0:
            raise ValidationError(errors)

        super(AbstractPost, self).clean(*args, **kwargs)
