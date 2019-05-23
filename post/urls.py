from post.views.post import PostViewSet
from post.views.bookmark import BookmarkViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path


post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update'
})

bookmark_list = BookmarkViewSet.as_view({
    'get':'list',
    'post':'create'
})

urlpatterns = format_suffix_patterns([
    path('', post_list, name='post-list'),
    path('<slug>/', post_detail, name='post-detail'),
    path('bookmark',bookmark_list,name='bookmark-list'),
])