from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
   url(r'^$', 'billing_record.views.index'),
   url(r'^2013/$', 'billing_record.views.index')
   #(r'^(?P<year>\d{4})/$', 'index'),
   #(r'^(?P<month>\d{2})/$', 'index'),
   #(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'index'),
)
