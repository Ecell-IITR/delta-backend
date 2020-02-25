from django.db import models
from django.core.exceptions import ValidationError
from utilities.models import WebsiteModel


class SocialLink(models.Model):
    def validate_image(image_obj):
        image_size = image_obj.file.size
        max_size = 150
        if image_size > max_size * 1024:
            raise ValidationError("Max Image Size is %sKB" % str(max_size))

    website = models.OneToOneField(WebsiteModel, on_delete=models.CASCADE)
    website_logo = models.ImageField(
        upload_to="social_link_logo/", default="null", validators=[validate_image]
    )

    def __str__(self):
        return self.website.website_name

