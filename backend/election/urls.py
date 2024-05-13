from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'info', views.ElectionInfoViewSet, 'election-info')
router.register(r'result', views.ElectionResultViewSet, 'election-result')

# order matters
urlpatterns = [
    path('vote/', views.vote, name='vote'),
    path('<slug:election_slug>/<slug:slug>/', views.CandidateAPIView.as_view(), name='candidate'),
]
urlpatterns += router.urls