from django.db import models

from utilities.models import TimestampedModel


class AbstractLocation(TimestampedModel):

    name = models.CharField(
        max_length=255,
        verbose_name="Location",
        help_text="Type the Location name to be added.."
    )

    state = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="State"
    )

    country = models.CharField(
        default='India',
        max_length=255,
        verbose_name='Country'
    )

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
