from django.conf import settings
from django.db import models
from users.models.time_stamped import TimestampedModel
from users.models.person import Person


class AbstractPost(TimestampedModel):
    """
    This model describes a Post who uses Omniport
    """

    slug = models.SlugField(
        db_index=True,
        unique=True,
        max_length=255
    )

    user = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='post'
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

    is_public = models.BooleanField(
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


class Post(AbstractPost):
    """
    This class implements AbstractPerson
    """

    class Meta:
        """
        Meta class for Person
        """

        verbose_name_plural = 'Post'
