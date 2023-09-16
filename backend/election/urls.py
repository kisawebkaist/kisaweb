from django.urls import path

from . import views

urlpatterns = [
    path('', views.election, name='election'),
    path('candidate/<str:name>', views.candidate, name='candidate'),
    path('candidate/<str:name>/vote', views.vote, name='vote'),
    path('candidate/change-embed-ratio/<pk>', views.change_embed_ratio, name='candidate_embed_ratio_change'),
    path('change-embed-ratio/', views.change_embed_ratio, name='debate_embed_ratio_change')
]
