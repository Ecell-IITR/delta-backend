from django.db import models
from users.models import Person
from utilities.models import TimestampedModel

from common.field_choices import USER_FIELD_CHOICES


class ActionUserRelation(TimestampedModel):
    action_on_person = models.ForeignKey(
        to=Person, related_name="action_on_person", on_delete=models.CASCADE)
    action_by_person = models.ForeignKey(
        to=Person, related_name="action_by_person", on_delete=models.CASCADE)
    action = models.PositiveIntegerField(
        choices=USER_FIELD_CHOICES.ACTIONS, default=USER_FIELD_CHOICES.FOLLOW)

    def __str__(self):
        return '%s-%s-%s' % (self.action_by_person.username, self.action, self.action_on_person.username)
