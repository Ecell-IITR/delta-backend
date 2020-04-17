from django.db import models
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver

from utilities.models import TimestampedModel


class Tag(TimestampedModel):
    title = models.CharField(max_length=128, db_index=True)
    hash = models.CharField(max_length=255, unique=True,
                            null=True, blank=True, db_index=True)

    def __str__(self):
        return self.title

    def get_admin_url(self, absolute=False):
        url = reverse('admin:%s_%s_change' % (
            self._meta.app_label, self._meta.model_name), args=[self.id])
        if absolute:
            url = settings.ADMIN_URL + url
        return url


@receiver(post_save, sender=Tag)
def create_tag(sender, instance=None, created=False, **kwargs):
    if created or instance.hash is None:
        instance.hash = get_random_string(8)
        instance.save()
