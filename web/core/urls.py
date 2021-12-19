from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    # path('important-links', views.important_links, name='important_links'),

    path('events/', include('events.urls')),
    path('election/', include('election.urls')),
    path('faq/', include('faq.urls')),
    path('docs/', include('docs.urls')),
    path('sso/', include('sso.urls')),
    path('blog/', include('blog.urls')),
    path('important-links/', include('important_links.urls')),
]
