from django.db import models
from django.core.validators import URLValidator
from utilities.models import TimestampedModel


def validate_image(image_obj):
    image_size = image_obj.file.size
    max_size = 150
    if image_size > max_size * 1024:
        raise ValidationError("Max Image Size is %sKB" % str(max_size))


class Website(TimestampedModel):

    name = models.CharField(max_length=155, verbose_name="Website Name")
    website_url = models.URLField(
        max_length=200, null=True, blank=True, validators=[URLValidator],
    )
    website_logo = models.ImageField(
        upload_to="social_link_logo/", default="null", validators=[validate_image]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "websites"
