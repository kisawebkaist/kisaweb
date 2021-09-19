from django.urls import path
import multimedia.views as views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='multimedia'),
    path('videos/<slug>', views.Video.as_view()), 
    path('images/<slug>', views.Image.as_view()), 
    # path('search', views.TagFilter.as_view()),
    path('<int:pk>', views.MultimediaView.as_view()), # Use pk instead of slug until slug field is implemented properly
]