from django.contrib import admin
from users.models.user import User
from users.models.profile import Profile

admin.site.register(User)
admin.site.register(Profile)
