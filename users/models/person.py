from django.db import models
from utilities.models import TimestampedModel
from django.contrib.auth.models import (
    AbstractUser
)

from common.get_file_path import get_profile_image_path

from users.managers import user
from users.constants import GET_ROLE_TYPE


class AbstractPerson(AbstractUser, TimestampedModel):
    """
    This model describes a person who uses Delta
    """
    username = models.CharField(
        db_index=True,
        max_length=50,
        verbose_name="Username",
        unique=True,
    )

    email = models.CharField(
        db_index=True,
        max_length=50,
        unique=True,
        verbose_name="Email/Company email",
        help_text="If you are company,enter Company email."
    )

    is_active = models.BooleanField(
        default=True
    )

    is_channeli_oauth = models.BooleanField(
        default=False
    )

    is_admin = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = user.UserManager()

    secondary_email = models.CharField(
        blank=True,
        db_index=True,
        max_length=50,
        verbose_name='Secondary Email'
    )

    profile_image = models.ImageField(
        upload_to=get_profile_image_path,
        help_text="If you are company,enter company icon.",
        blank=True,
        null=True,
        default='defaults/profile-image.png'
    )

    role_type = models.CharField(
        max_length=255,
        default=GET_ROLE_TYPE.STUDENT,
        verbose_name="User role"
    )

    class Meta:
        """
        Meta class for AbstractPerson
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        username = self.username
        email = self.email
        return '%s-%s' % (username, email)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Person(AbstractPerson):
    """
    This class implements AbstractPerson
    """

    class Meta:
        """
        Meta class for Person
        """

        verbose_name_plural = 'User'