from django.contrib import admin
from django import forms
from post.models import Competition, Internship, Project, AppliedPostEntries
from utilities.models import Tag


class InternshipAdminForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        self.request = request if request else self.request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        obj = self.instance
        request = self.request

        errors = {}

        if len(errors) > 0:
            raise ValidationError(errors)

        self.instance = obj
        return cleaned_data


class InternshipAdmin(admin.ModelAdmin):
    form = InternshipAdminForm
    list_display = ("title", "description", "is_verified", "is_published")
    readonly_fields = ("slug", "created_at", "updated_at")

    def get_changelist_form(self, request, **kwargs):
        class AdminFormWithRequest(InternshipAdminForm):
            def __init__(self, *args, **_kwargs):
                _kwargs["request"] = request
                super().__init__(*args, **_kwargs)

        kwargs.setdefault("form", AdminFormWithRequest)
        return super().get_changelist_form(request, **kwargs)

    def get_form(self, request, *args, **kwargs):
        form = super(InternshipAdmin, self).get_form(request, *args, **kwargs)
        form.request = request
        return form


admin.site.register(Internship, InternshipAdmin)


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        self.request = request if request else self.request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        obj = self.instance
        request = self.request

        errors = {}

        if len(errors) > 0:
            raise ValidationError(errors)

        self.instance = obj
        return cleaned_data


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ("title", "description", "is_verified", "is_published")
    readonly_fields = ("slug", "created_at", "updated_at")

    def get_changelist_form(self, request, **kwargs):
        class AdminFormWithRequest(ProjectAdminForm):
            def __init__(self, *args, **_kwargs):
                _kwargs["request"] = request
                super().__init__(*args, **_kwargs)

        kwargs.setdefault("form", AdminFormWithRequest)
        return super().get_changelist_form(request, **kwargs)

    def get_form(self, request, *args, **kwargs):
        form = super(ProjectAdmin, self).get_form(request, *args, **kwargs)
        form.request = request
        return form


admin.site.register(Project, ProjectAdmin)


class CompetitionAdminForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        self.request = request if request else self.request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        obj = self.instance
        request = self.request

        errors = {}

        if len(errors) > 0:
            raise ValidationError(errors)

        self.instance = obj
        return cleaned_data


class CompetitionAdmin(admin.ModelAdmin):
    form = CompetitionAdminForm
    list_display = ("title", "description", "is_verified", "is_published")
    readonly_fields = ("slug", "created_at", "updated_at")

    def get_changelist_form(self, request, **kwargs):
        class AdminFormWithRequest(CompetitionAdminForm):
            def __init__(self, *args, **_kwargs):
                _kwargs["request"] = request
                super().__init__(*args, **_kwargs)

        kwargs.setdefault("form", AdminFormWithRequest)
        return super().get_changelist_form(request, **kwargs)

    def get_form(self, request, *args, **kwargs):
        form = super(CompetitionAdmin, self).get_form(request, *args, **kwargs)
        form.request = request
        return form


admin.site.register(Competition, CompetitionAdmin)


class AppliedPostEntriesAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    readonly_fields = ("created_at", "updated_at")


admin.site.register(AppliedPostEntries, AppliedPostEntriesAdmin)
