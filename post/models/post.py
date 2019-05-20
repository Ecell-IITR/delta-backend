from django.db import models
from users.models.profile import Profile

# Create your models here.


class Post(models.Model):
    COMPETITION_TYPE = (
        ('online', 'online'),
        ('onspot', 'onspot')
    )
    WORK_TYPE = {
        ('Full time', 'Full time'),
        ('Part time', 'Part time')
    }
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='post')
    company_name = models.CharField(
        max_length=100, verbose_name="Company name")
    company_domain = models.CharField(
        max_length=255, verbose_name="Company domain")
    description = models.TextField(verbose_name="Description")
    work_location = models.CharField(
        max_length=100, verbose_name="Work location")
    start_date = models.DateTimeField(verbose_name="Start date")
    completition_date = models.DateTimeField(verbose_name="completion date")
    post_expiry_date = models.DateTimeField(verbose_name="Post expiry date")
    appicant_numbers = models.IntegerField(default=0, blank=True, null=True)
    competition_type = models.CharField(max_length=255,
                                        choices=COMPETITION_TYPE, default='onspot', verbose_name="Competition type")
    work_type = models.CharField(max_length=255,
                                 choices=WORK_TYPE, default='part time', verbose_name="Work type")
    work_description = models.TextField(verbose_name="Work Description")
    stipend = models.FloatField(blank=True, null=True, default=0)
    required_skill = models.TextField(verbose_name="Required skill Set")
    product_detail = models.TextField(verbose_name="product detail")


def __str__(self):
    return self.company_name
