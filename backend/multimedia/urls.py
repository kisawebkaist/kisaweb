from django.urls import path
import multimedia.views as views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='multimedia'),
    path('pages/<slug:slug>/', views.MultimediaView.as_view()),
]