from django.conf.urls.static import static
from django.conf.urls.defaults import patterns, url, include

from django.contrib import admin
from admin_apps.settings import local as settings
from tastypie.api import Api
from api import BillingRecordResource, UserResource

admin.autodiscover()

api = Api(api_name='api')
api.register(UserResource())
api.register(BillingRecordResource())

urlpatterns = patterns('',
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^logout/$', 'billing_record.views.logout_page'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^billing/', include('billing_record.urls')),
    (r'^a/', include(api.urls)),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
