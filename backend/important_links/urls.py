from rest_framework.routers import DefaultRouter
from .views import LinkCategoryViewset, LinkViewset

router = DefaultRouter()
router.register(
    'categories', LinkCategoryViewset, basename = 'important-links-category'
)
router.register(
    '', LinkViewset, basename = 'important-links'
)

urlpatterns = router.urls
