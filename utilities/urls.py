from django.urls import path, include
from utilities.views import SkillsAPIView

urlpatterns = [
    path('skills/', SkillsAPIView.as_view(), name="register"),
]
