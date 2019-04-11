from post.views.views import PostViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register(r'post', PostViewSet, base_name='post')

urlpatterns = router.urls
