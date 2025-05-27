from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

urlpatterns = [
    path('member-list/', views.CurrentKISAMemberListView.as_view(), name='aboutus-member-list'),
    path('me/', views.MyKISAMemberView.as_view(), name='aboutus-me'),
]

router = SimpleRouter()
router.register(
    r'divisions', views.KISADivisionContentViewset, basename = 'aboutus-divisions'
)

urlpatterns += router.urls
