from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from utilities.models import Website

class SocialLink(models.Model):

    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    profile_url = models.URLField(
        max_length=200, validators=[URLValidator],
    )    

    class Meta:
        verbose_name_plural = "Social Links"
    
    def __str__(self):
        return self.website.name
