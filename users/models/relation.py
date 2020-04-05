from django.db import models
from users.models import Person
from utilities.models import TimestampedModel


class AbstractUserRelationship(TimestampedModel):
    REL_CHOICES = (
        ('follow', "Follow"),
        ("likes", "Likes"),
        ("bookmark", "Bookmarks")
    )
    user_from = models.ForeignKey(
        to=Person, related_name="rel_from", on_delete=models.CASCADE)
    user_to = models.ForeignKey(
        to=Person, related_name="rel_to", on_delete=models.CASCADE)
    rel_type = models.CharField(
        max_length=10, choices=REL_CHOICES, default="follow")

    def __str__(self):
        return f'{self.user_from} {self.rel_type} {self.user_to}'

    class Meta:
        abstract = True
        unique_together = ('user_from', 'rel_type', 'user_to')


class UserRelationship(AbstractUserRelationship):
    class Meta:
        verbose_name_plural = "Relationship"
