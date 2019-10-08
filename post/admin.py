from django.contrib import admin
from post.models.post_roles import (
    Competition,
    Internship,
    Project
)

models = [
    Competition,
    Internship,
    Project,
]

for model in models:
    admin.site.register(model)
