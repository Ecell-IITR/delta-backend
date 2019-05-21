from django.db import models
from users.models.user import User
from users.models.time_stamped import TimestampedModel


class ProfileManager(models.Manager):
    pass


class Profile(TimestampedModel):
    USER_TYPE = (
        ('Company', 'Company'),
        ('Student', 'Student')
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )

    user_type = models.CharField(
        max_length=20, choices=USER_TYPE, default='Student', verbose_name='User type')
    branch = models.CharField(
        max_length=55, blank=True, verbose_name='Branch')
    enrollment_number = models.CharField(
        max_length=20, blank=True, verbose_name='Enrollment number')
    year = models.CharField(
        max_length=55, blank=True, verbose_name='Year')
    social_links = models.TextField(blank=True, verbose_name='Social links')
    skills = models.TextField(blank=True, verbose_name='Skills')
    interest = models.TextField(blank=True, verbose_name='Interest')
    bio = models.TextField(verbose_name='Bio', blank=True)
    achievements = models.TextField(verbose_name='Achievements', blank=True)
    profile_image = models.ImageField(
        upload_to="profile_image/", default="null")

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User profile"
