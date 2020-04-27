from django.db import models
from django.core.validators import RegexValidator
from users.models.person import Person
from users.models.roles.social_link import SocialLink
from django.core.validators import FileExtensionValidator

class AbstractStudent(models.Model):

    person = models.OneToOneField(to=Person, on_delete=models.CASCADE, related_name="student_profile")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    branch = models.ForeignKey(
        to="utilities.Branch",
        related_name="student_branch",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[
            RegexValidator(regex="^[6-9]\d{9}$",
                           message="Phone Number Not Valid",)
        ],
    )
    enrollment_number = models.CharField(max_length=20, blank=True, verbose_name="Enrollment number")
    course = models.CharField(max_length=55, blank=True, verbose_name="Course")
    year = models.CharField(max_length=55, blank=True, verbose_name="Year")
    social_links = models.ManyToManyField(to=SocialLink, related_name="social_links", blank=True)
    skills = models.ManyToManyField(to="utilities.Skill", related_name="student_skill", blank=True)
    interest = models.TextField(blank=True, verbose_name="Interest")
    bio = models.TextField(verbose_name="Bio", blank=True)
    achievements = models.TextField(verbose_name="Achievements", blank=True)
    resume = models.FileField(verbose_name="Resume", blank=True, validators=[
                              FileExtensionValidator(allowed_extensions=['pdf'])])
    availability_status = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     input_resume=open(resume,"wb")
    #     s=input_resume.read()

    class Meta:
        """
        Meta class for AbstractStudent
        """

        abstract = True

    def __str__(self):
        person = self.person
        return f"{person}"


class Student(AbstractStudent):

    class Meta:
        """
        Meta class for Student
        """

        verbose_name_plural = "Student"
