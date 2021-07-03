from django.urls import path
import multimedia.views as views

urlpatterns = [
    path('videos/<slug>', views.Video.as_view()), 
    path('images/<slug>', views.Image.as_view()), 
    path('multimedia/<slug>', views.Multimedia.as_view()),
    path('multimedia/home', views.HomePage.as_view()),
    path('multimedia/search', views.TagFilter.as_view())
]