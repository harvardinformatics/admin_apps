from django.conf.urls.static import static
from django.conf.urls.defaults import patterns, url, include

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
   # (r'', include('admin_apps.apps.')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)