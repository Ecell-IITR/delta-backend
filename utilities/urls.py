from django.urls import path, include
from utilities.views import SkillsAPIView

urlpatterns = [
    path('skills/', SkillsAPIView.as_view(), name="skills-list"),
    # path('tags/autocomplete/', TagsAutoComplete.as_view(), name="tags-autocomplete"),
]
