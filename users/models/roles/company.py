from django.db import models
from django.core.validators import RegexValidator

from users.models.person import Person
from users.constants import GET_ROLE_TYPE

class AbstractCompany(models.Model):
    """
    This model holds information pertaining to a company
    """

    person = models.OneToOneField(
        to=Person, on_delete=models.CASCADE, related_name="company"
    )

    company_domain = models.CharField(
        max_length=55, blank=True, verbose_name="Company Domain"
    )
    phone_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[
            RegexValidator(regex="^[6-9]\d{9}$", message="Phone Number Not Valid",)
        ],
    )
    category_of_company = models.CharField(
        blank=True, max_length=50, verbose_name="Category of Company"
    )
    team_size = models.CharField(blank=True, max_length=100, verbose_name="Team size")
    address = models.TextField(blank=True, verbose_name="Address")

    class Meta:
        """
        Meta class for AbstractCompany
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.person
        return f"{person}"

    def clean(self, *args, **kwargs):
        errors = {}
        if hasattr(self, 'person') and self.person:
            if self.person.role_type != GET_ROLE_TYPE.COMPANY:
                errors.setdefault('person', []).append(
                    'Person object has role_type equal to company.')

        if len(errors) > 0:
            raise ValidationError(errors)

        super(AbstractPost, self).clean(*args, **kwargs)



class Company(AbstractCompany):
    """
    This class implements AbstractCompany
    """

    class Meta:
        """
        Meta class for Company
        """
        verbose_name_plural = "Company"

