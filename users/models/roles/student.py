from django.db import models
from users.models.person import Person


class AbstractStudent(models.Model):
    """
    This model holds information pertaining to a student
    """

    person = models.OneToOneField(
        to=Person,
        on_delete=models.CASCADE,
        related_name='student'
    )

    branch = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Branch'
    )

    enrollment_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Enrollment number'
    )

    course = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Course'
    )

    year = models.CharField(
        max_length=55,
        blank=True,
        verbose_name='Year'
    )

    social_links = models.TextField(
        blank=True,
        verbose_name='Social links'
    )

    starred_posts = models.ManyToManyField(
        to='post.Post',
        related_name='starred_post_set',
        blank=True
    )

    skills = models.TextField(
        blank=True,
        verbose_name='Skills'
    )

    interest = models.TextField(
        blank=True,
        verbose_name='Interest'
    )

    bio = models.TextField(
        verbose_name='Bio',
        blank=True
    )

    achievements = models.TextField(
        verbose_name='Achievements',
        blank=True
    )

    class Meta:
        """
        Meta class for AbstractStudent
        """

        abstract = True

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        person = self.person
        return f'{person}'


class Student(AbstractStudent):
    """
    This class implements AbstractStudent
    """

    class Meta:
        """
        Meta class for Student
        """
        verbose_name_plural = 'Student'
