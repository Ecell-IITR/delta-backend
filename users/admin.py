from django.contrib import admin
from users.models.roles import Student, Company
from users.models.person import Person


models = [
    Person,
    Company,
    Student,
]

for model in models:
    admin.site.register(model)
