from django.contrib import admin
from users.models.roles import Student, Company
from users.models.person import Person
from users.models.social_link import SocialLink

models = [
    Person,
    Company,
    Student,
    SocialLink,
]

for model in models:
    admin.site.register(model)
