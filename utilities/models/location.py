from django.db import models

from utilities.models import TimestampedModel, Country, State


class AbstractLocation(TimestampedModel):

    name = models.CharField(
        max_length=255,
        verbose_name="Location",
        help_text="Type the Location name to be added.."
    )

    state = models.OneToOneField(
        to=State, on_delete=models.CASCADE
    )

    country = models.OneToOneField(
        to=Country, on_delete=models.CASCADE
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
