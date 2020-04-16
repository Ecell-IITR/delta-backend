from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.core.exceptions import ValidationError

from utilities.models import TimestampedModel
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
        on_delete=models.CASCADE
    )

    title = models.CharField(
        default="title",
        max_length=100,
        verbose_name="Title"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )

    post_expiry_date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name="Post expiry date"
    )

    required_skill = models.TextField(
        blank=True,
        verbose_name="Required skill Set"
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name="Published"
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name="Verified"
    )

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
