from django.urls import path
import multimedia.views as views

urlpatterns = [
    path('home/', views.HomePageView.as_view(), name='multimedia'),
    # path('search', views.TagFilter.as_view()),
    path('pages/<slug:slug>', views.MultimediaView.as_view()),
]