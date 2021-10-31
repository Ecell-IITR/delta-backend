from django.db import models
from utilities.models import TimestampedModel


class AbstractCountry(TimestampedModel):
    name = models.CharField(max_length=255, verbose_name="Country", default="India")

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        return self.name

    class Meta:
        abstract = True


class Country(AbstractCountry):
    class Meta:
        verbose_name_plural = "Country"
