from django.urls import path, include

from utilities.views import SkillsAPIView, SkillAddAPI, SkillRemoveAllAPI, SkillRemoveAPI, LocationsListAPI, SocialLinksWebsitesAPIView, TagsListAPI, SkillSearchsAPIView


urlpatterns = [
    path(r'skills/', SkillsAPIView.as_view(), name="skills-list"),
    path(r'skills_search/', SkillSearchsAPIView.as_view(), name="skills-search"),
    path(r'social_links_websites/', SocialLinksWebsitesAPIView.as_view(), name="social-links-list"),
    path(r'skills/add/<slug:slug>/', SkillAddAPI.as_view(), name="skill-add"),
    path(r'skills/remove/<slug:slug>/', SkillRemoveAPI.as_view(), name="skill-remove"),
    path(r'skills/remove-all/', SkillRemoveAllAPI.as_view(), name="skills-remove-all"),
    path(r'locations_list/', LocationsListAPI.as_view(), name="locations-list"),
    path(r'tags_list/', TagsListAPI.as_view(), name="tags-list"),
   
    # path('tags/autocomplete/', TagsAutoComplete.as_view(), name="tags-autocomplete"),
]
