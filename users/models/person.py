from django.db import models
from utilities.models import TimestampedModel
from django.contrib.auth.models import (
    AbstractUser
)
from users.managers import user


class AbstractPerson(AbstractUser, TimestampedModel):
    """
    This model describes a person who uses Delta
    """
    username = models.CharField(
        db_index=True,
        max_length=50,
        verbose_name="Username/Company Name",
        unique=True,
        help_text="If you are company,enter Company name."
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
        upload_to="profile_image/",
        default="null",
        help_text="If you are company,enter company icon."
    )

    is_company = models.BooleanField(
        default=False
    )

    is_student = models.BooleanField(
        default=False
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
        return f'{username}-{email}'

    def has_perm(self, perm, obj=None):
        """
        Add an alternative check to the default check for permissions
        :param perm: the permission to check for
        :param obj: the object on which to check permissions instead of self
        :return: True if the user is an administrative IMGian, false otherwise
        """

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
