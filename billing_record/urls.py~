from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('billing_record.views',
   #web
   url(r'^$', 'index'),
   #pdf
   url(r'^pdf/$', 'pdf'),

   (r'^generate_doc/$', 'generate_doc'),
   (r'^generate_doc/(?P<file_format>\w+)/$', 'generate_doc'),

)
