"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('grappelli/', include('grappelli.urls')), # grappelli URLS
    # path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('docs/', include('docs.urls')),
    path('multimedia/', include('multimedia.urls')),
    path('important-links/', include('important_links.urls')),
    path('alumni/', include('alumni.urls')),
    path(f'{settings.URL_SHORTENER_PREFIX}/', include('url_shortener.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('maintenance-mode/', include('maintenance_mode.urls')),

    # CONVERTED
    path('api/about-us/', include('aboutus.urls')),
    path('api/faq/', include('faq.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/sso', include('sso.urls'))
    path('api/election', include('election.urls'))
]

# Add static file urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add media file urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
