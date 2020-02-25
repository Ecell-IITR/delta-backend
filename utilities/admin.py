from django.contrib import admin

from utilities.models import (
    Skill,
    Branch,
    Location,
    WebsiteModel
)

models = [
    Skill,
    Branch,
    Location,
    WebsiteModel
]

for model in models:
    admin.site.register(model)
