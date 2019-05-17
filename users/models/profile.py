from django.db import models
from users.models.user import User


class ProfileManager(models.Manager):
    pass


class Profile(models.Model):
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
    profile_image = models.URLField(verbose_name='Profile image', blank=True)
    updated_at = models.DateTimeField(
        verbose_name='Last Updated', auto_now=True, null=True)
    created_at = models.DateTimeField(
        verbose_name='Date Joined', auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User profile"
