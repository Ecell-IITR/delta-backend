from django.contrib import admin

from utilities.models import Skill, Branch, Location, Website, State, Country, Tag

models = [Skill, Branch, Location, Website, State, Country]

for model in models:
    admin.site.register(model)


class TagAdmin(admin.ModelAdmin):
    list_display = ('hash', 'title')
    search_fields = ('title',)
    readonly_fields = ('hash', 'created_at', 'updated_at')


admin.site.register(Tag, TagAdmin)
