from post.views.post import PostViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)

router.register(r'', PostViewSet)

urlpatterns = router.urls
