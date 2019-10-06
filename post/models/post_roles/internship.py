from django.db import models
from users.models.time_stamped import TimestampedModel
from post.models.post import Post

WORK_TYPE = {
    (
        'Full time', 'Full time'
    ),
    (
        'Part time', 'Part time'
    )
}


class AbstractInternship(models.Model):
    """
    This model holds information pertaining to a Internship
    """

    post = models.OneToOneField(
        to=Post,
        on_delete=models.CASCADE,
    )

    stipend = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Stipend'
    )

    position = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Position'
    )

    duration = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Duration'
    )

    product_details = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Product Details'
    )

    work_type = models.CharField(
        max_length=255,
        choices=WORK_TYPE,
        default='part time',
        verbose_name="Type of Work"
    )

    class Meta:
        """
        Meta class for AbstractInternship
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        post = self.post
        return f'{post}'


class Internship(AbstractInternship):
    """
    This class implements AbstractInternship
    """

    class Meta:
        """
        Meta class for Internship
        """
        verbose_name_plural = 'Internship'
