from django.db import models
from django.core.validators import URLValidator
from utilities.models import TimestampedModel


class WebsiteModel(TimestampedModel):

    website_name = models.CharField(max_length=155, verbose_name="Website")
    website_url = models.URLField(
        max_length=200, null=True, blank=True, validators=[URLValidator],
    )

    def __str__(self):
        return self.website_name

    class Meta:
        verbose_name_plural = "websites"
