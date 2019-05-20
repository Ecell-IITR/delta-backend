from post.views.post import PostViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)

router.register(r'post', PostViewSet)

urlpatterns = router.urls
