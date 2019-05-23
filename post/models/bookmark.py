from django.db import models
from users.models.profile import Profile
from users.models.time_stamped import TimestampedModel
from post.models.post import Post

class Bookmark(TimestampedModel):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='bookmark')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.author