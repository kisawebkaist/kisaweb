from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(
    '', views.MultimediaViewSet, basename = 'multimedia'
)

urlpatterns = router.urls