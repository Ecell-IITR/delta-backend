from django.db import models
from django.core.validators import URLValidator
from utilities.models import TimestampedModel
from django.core.exceptions import ValidationError

from common.get_file_path import get_website_logo_image_path


def validate_image(image_obj):
    image_size = image_obj.file.size
    max_size = 150
    if image_size > max_size * 1024:
        raise ValidationError("Max Image Size is %sKB" % str(max_size))


class Website(TimestampedModel):

    name = models.CharField(max_length=155, verbose_name="Website Name")
    website_url = models.URLField(
        max_length=200,
        null=True,
        blank=True,
        validators=[URLValidator],
    )
    website_logo = models.ImageField(
        upload_to=get_website_logo_image_path,
        validators=[validate_image],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "Websites"

    def __str__(self):
        return self.name
