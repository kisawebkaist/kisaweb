from django.urls import path
import multimedia.views as views

urlpatterns = [
    path('videos/<slug>', views.Video.as_view()), 
    path('images/<slug>', views.Image.as_view()), 
    path('home', views.HomePageView.as_view()),
    path('search', views.TagFilter.as_view()),
    path('<slug>', views.MultimediaView.as_view()),
]