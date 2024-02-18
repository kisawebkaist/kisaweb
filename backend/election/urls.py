from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'info', views.ElectionInfoViewSet, 'election-info')
router.register(r'result', views.ElectionResultViewSet, 'election-result')

urlpatterns = [
    path('<str:election_slug>/<str:slug>/', views.CandidateAPIView.as_view(), name='candidate')
]
urlpatterns += router.urls