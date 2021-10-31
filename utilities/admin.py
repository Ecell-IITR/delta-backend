from django.contrib import admin

from utilities.models import (
    Skill,
    Branch,
    Location,
    Website,
    State,
    Country,
    Tag,
    SkillType,
)

models = [Branch, Website, State, Country]

for model in models:
    admin.site.register(model)


class TagAdmin(admin.ModelAdmin):
    list_display = ("hash", "title")
    search_fields = ("title",)
    readonly_fields = ("hash", "created_at", "updated_at")


admin.site.register(Tag, TagAdmin)


class SkillAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "type")
    readonly_fields = ("slug", "created_at", "updated_at")


admin.site.register(Skill, SkillAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "state", "country", "pin_code")
    readonly_fields = ("slug", "created_at", "updated_at")


admin.site.register(Location, LocationAdmin)


class SkillTypeAdmin(admin.ModelAdmin):
    list_display = ("type",)
    readonly_fields = ("created_at", "updated_at")


admin.site.register(SkillType, SkillTypeAdmin)
