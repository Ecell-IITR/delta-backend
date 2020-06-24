from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from utilities.models import TimestampedModel


class AppliedPostEntries(TimestampedModel):

    user_limit = models.Q(app_label='users', model='student') | models.Q(
        app_label='users', model='company')
    user_content_type = models.ForeignKey(
        ContentType, related_name='applied_user_entries_post', on_delete=models.CASCADE, limit_choices_to=user_limit)
    user_object_id = models.PositiveIntegerField()
    user = GenericForeignKey('user_content_type', 'user_object_id')

    post_limit = models.Q(app_label='post', model='internship') | models.Q(
        app_label='post', model='competition') | models.Q(app_label='post', model='project')
    post_content_type = models.ForeignKey(
        ContentType, related_name='applied_post_entries_post', on_delete=models.CASCADE, limit_choices_to=post_limit)
    post_object_id = models.PositiveIntegerField(
        verbose_name='Post Object Id')
    post = GenericForeignKey('post_content_type', 'post_object_id')

    def __str__(self):
        user = self.user
        post = self.post
        return '%s - %s' % (user, post)

    class Meta:

        verbose_name_plural = 'Applied Post Entries'
