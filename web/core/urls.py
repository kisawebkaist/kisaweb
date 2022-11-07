from django.urls import path, include

from web.settings import URL_SHORTENER_PREFIX

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    # path('important-links', views.important_links, name='important_links'),

    path('events/', include('events.urls')),
    path('election/', include('election.urls')),
    path('faq/', include('faq.urls')),
    path('docs/', include('docs.urls')),
    path('sso/', include('sso.urls')),
    path('about-us/', include('aboutus.urls')),
    path('multimedia/', include('multimedia.urls')),
    path('blog/', include('blog.urls')),
    path('important-links/', include('important_links.urls')),
    path(f'{URL_SHORTENER_PREFIX}/', include('url_shortener.urls')),
]
