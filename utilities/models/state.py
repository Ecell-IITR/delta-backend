from django.db import models
from utilities.models import TimestampedModel, Country


class AbstractState(TimestampedModel):
    name = models.CharField(max_length=255, verbose_name="State")

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """
        name = self.name
        return "%s" % name

    class Meta:
        abstract = True


class State(AbstractState):
    class Meta:
        verbose_name_plural = "State"
