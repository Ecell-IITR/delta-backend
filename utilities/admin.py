from django.contrib import admin

from utilities.models import (
    Skill,
    Branch
)

models = [
    Skill,
    Branch
]

for model in models:
    admin.site.register(model)
