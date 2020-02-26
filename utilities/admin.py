from django.contrib import admin

from utilities.models import Skill, Branch, Location, Website

models = [Skill, Branch, Location, Website]

for model in models:
    admin.site.register(model)
