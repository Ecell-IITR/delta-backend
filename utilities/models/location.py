from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from post.utils import unique_slug_generator

from utilities.models import TimestampedModel, Country, State


class AbstractLocation(TimestampedModel):
    
    slug = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Location",
        help_text="Type the Location name to be added.."
    )
    state = models.ForeignKey(State, related_name="state", on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, related_name="country", on_delete=models.DO_NOTHING)
    pin_code = models.IntegerField(
        unique=True,
        verbose_name='Pincode'
    )

    def __str__(self):
        """
       Return the string representation of the model
       :return: the string representation of the model
       """

        name = self.name
        pin_code = self.pin_code
        return f'{name} - {pin_code}'

    class Meta:
        """
        Meta class for AbstractLocation
        """

        abstract = True


class Location(AbstractLocation):
    """
    This class implements AbstractLocation
    """

    class Meta:
        """
        Meta class for Location
        """

        verbose_name_plural = 'Location'


@receiver(post_save, sender=AbstractLocation)
def create_location(sender, instance=None, created=False, **kwargs):
    if created or instance.slug is None:
        instance.slug = unique_slug_generator(instance, 'name')
        instance.save()