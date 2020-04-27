from django.urls import path, include
from utilities.views import SkillsAPIView, SkillAddAPI, SkillRemoveAllAPI, SkillRemoveAPI

urlpatterns = [
    path(r'skills/', SkillsAPIView.as_view(), name="skills-list"),
    path(r'skills/add/<slug:slug>/', SkillAddAPI.as_view(), name="skill-add"),
    path(r'skills/remove/<slug:slug>/', SkillRemoveAPI.as_view(), name="skill-remove"),
    path(r'skills/remove-all/', SkillRemoveAllAPI.as_view(), name="skills-remove-all"),
    # path('tags/autocomplete/', TagsAutoComplete.as_view(), name="tags-autocomplete"),
]
