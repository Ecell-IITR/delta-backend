from django.db import models
from users.models import Person
from utilities.models import TimestampedModel


class AbstractFollowUser(TimestampedModel):

    follower = models.ForeignKey(
        to=Person, related_name="follow_to", on_delete=models.CASCADE)
    following = models.ForeignKey(
        to=Person, related_name="followed_by", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

    class Meta:
        abstract = True
        unique_together = ('follower', 'following')


class FollowUser(AbstractFollowUser):
    class Meta:
        verbose_name_plural = "Follow"
