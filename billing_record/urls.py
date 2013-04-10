from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('billing_record.views',
   #web
   url(r'^$', 'index'),
   #pdf
   url(r'^pdf/$', 'pdf'),

   url(r'^generate_html_doc/$', 'generate_html_doc'),
   #url(r'^generate_pdf_doc/$', 'generate_pdf_doc'),

)
