from django.contrib import admin
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import admin as auth_admin

from users.models.roles import Student, Company
from users.models.person import Person


class PersonChangeForm(forms.ModelForm):
    """
    Replicate the form shown when the user model supplied by Django is not
    replaced with our own by copying most of the code
    """
    password = auth_forms.ReadOnlyPasswordHashField(
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"../password/\">this form</a>.",
    )

    class Meta:
        """
        Meta class for PersonChangeForm
        """

        model = Person
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PersonChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class PersonAdmin(auth_admin.UserAdmin):

    form = PersonChangeForm

    fieldsets = (
        ('Authentication', {
            'fields': (
                'username',
                'password',
                'email'
            )
        }),
        ('Important dates', {
            'fields': (
                'last_login',
            )
        }),
        ('Permissions', {
            'fields': (
                'is_superuser',
                'user_permissions',
            )
        }),
    )

    list_display = (
        'username',
        'email',
        'last_login',
        'is_company',
        'is_student'
    )
    list_filter = tuple()

    search_fields = ['id', 'email']


admin.site.register(Person, PersonAdmin)

models = [
    Company,
    Student,
]

for model in models:
    admin.site.register(model)
