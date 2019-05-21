from django.db import models
from users.models.profile import Profile 
from users.models.time_stamped import TimestampedModel
from django.db.models.signals import pre_save
from post.utils import unique_slug_generator
class Post(TimestampedModel):
    COMPETITION_TYPE = (
        ('online', 'online'),
        ('onspot', 'onspot')
    )
    WORK_TYPE = {
        ('Full time', 'Full time'),
        ('Part time', 'Part time')
    }
    slug = models.SlugField(db_index=True, max_length=255)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(default="title",
        max_length=100, verbose_name="Tiltle")
    description = models.TextField(blank=True, verbose_name="Description")
    work_location = models.CharField(blank=True,
                                     max_length=100, verbose_name="Work location")
    start_date = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Start date")
    completition_date = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="completion date")
    post_expiry_date = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Post expiry date")
    appicant_numbers = models.IntegerField(default=0, blank=True)
    competition_type = models.CharField(max_length=255,
                                        choices=COMPETITION_TYPE, default='onspot', verbose_name="Competition type")
    work_type = models.CharField(max_length=255,
                                 choices=WORK_TYPE, default='part time', verbose_name="Work type")
    work_description = models.TextField(
        blank=True, verbose_name="Work Description")
    stipend = models.FloatField(blank=True, default=0)
    required_skill = models.TextField(
        blank=True, verbose_name="Required skill Set")
    product_detail = models.TextField(
        blank=True, verbose_name="product detail")
    is_public = models.BooleanField(default=False, verbose_name="Published")
    is_verified = models.BooleanField(default=False, verbose_name ="Verified")

    def __str__(self):
        return self.title


def pre_save_receiver(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_slug_generator(instance) 
  
  
pre_save.connect(pre_save_receiver, sender = Post)