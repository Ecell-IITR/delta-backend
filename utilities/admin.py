from django.contrib import admin

from utilities.models import (
    Skill,
    Branch,
    Location
)

models = [
    Skill,
    Branch,
    Location
]

for model in models:
    admin.site.register(model)
