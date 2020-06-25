from django.db import models
from django.db.models.signals import post_save, pre_save
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
        return '%s - %s' % (name, pin_code)

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


@receiver(pre_save, sender=Location)
def location_pre_save(instance=None, created=False, update_fields=None, **kwargs):
    location = None
    if not created and update_fields is None:
        try:
            location = Location.objects.get(pk=instance.pk)
        except Location.DoesNotExist:
            pass
    instance.__old_instance = location


@receiver(post_save, sender=Location)
def location_post_save(update_fields, instance=None, created=False, **kwargs):
    if update_fields is None:
        old_inst = instance.__old_instance
        if old_inst is None or old_inst.name != instance.name:
            instance.slug = unique_slug_generator(instance, 'name')
            instance.save()