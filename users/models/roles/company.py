from django.db import models
from django.core.validators import RegexValidator
from users.models.person import Person


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


class Company(AbstractCompany):
    """
    This class implements AbstractCompany
    """

    class Meta:
        """
        Meta class for Company
        """
        verbose_name_plural = "Company"

