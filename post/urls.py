from django.urls import path, include

from post.views import (
    PostViewSet,
    BookmarkView,
    CreatePost,
    ApplyPostView,
)

Post = PostViewSet.as_view({
    'get': 'list'
})

IndividualPost = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path(r'create/', CreatePost.as_view()),
    path(r'', Post),
    path(r'<slug:slug>/', IndividualPost),
    path(r'apply/<slug:slug>/', ApplyPostView.as_view()),
    path(r'bookmark/<slug:slug>/', BookmarkView.as_view())
]
