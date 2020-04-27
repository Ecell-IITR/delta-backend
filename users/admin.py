from django.contrib import admin
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import admin as auth_admin

from users.models.roles import Student, Company, SocialLink
from users.models.person import Person
from users.models.relation import FollowUser


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
        ('Information', {
            'fields': (
                'role_type',
                'secondary_email',
                'profile_image'
            )
        }),
    )

    list_display = (
        'username',
        'email',
        'last_login',
        'role_type',
    )
    readonly_fields = ('role_type', )
    list_filter = tuple()

    search_fields = ['id', 'email', 'username']


admin.site.register(Person, PersonAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'availability_status')


admin.site.register(Student, StudentAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_domain', 'phone_number')


admin.site.register(Company, CompanyAdmin)


# models = [
#     SocialLink


class FollowUserAdmin(admin.ModelAdmin):
    list_display = (
        'follower',
        'following'
    )


admin.site.register(FollowUser, FollowUserAdmin)

models = [

    SocialLink,

]

for model in models:
    admin.site.register(model)
