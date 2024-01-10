from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

# urlpatterns = [
#     path('', views.aboutus, name='aboutus'),
# ]

router = DefaultRouter()
router.register(
  r'members', views.MemberViewset, basename = 'aboutus-members'
)
router.register(
  r'internal-members', views.InternalBoardMemberViewset,
  basename = 'aboutus-internal-members'
)
router.register(
  r'divisions', views.DivisionViewset, basename = 'aboutus-divisions'
)
urlpatterns = router.urls
