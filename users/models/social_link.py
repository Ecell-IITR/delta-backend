from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from utilities.models import Website


class SocialLink(models.Model):

    website = models.OneToOneField(Website, on_delete=models.CASCADE)
    profile_url = models.URLField(
        max_length=200, validators=[URLValidator],
    )

    def __str__(self):
        return self.website.name
