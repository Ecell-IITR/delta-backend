from django.contrib import admin
from users.models.roles import Student, Company
from users.models.person import Person
# from users.models.custom_user import User


models = [
    # User,
    Person,
    Company,
    Student,
]

for model in models:
    admin.site.register(model)
