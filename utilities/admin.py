from django.contrib import admin

from utilities.models import Skill, Branch, Location, Website, State, Country

models = [Skill, Branch, Location, Website, State, Country]

for model in models:
    admin.site.register(model)
