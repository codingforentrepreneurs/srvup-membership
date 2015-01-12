from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    #url(r'^about/$', TemplateView.as_view(template_name='base.html'), name='home'),
    #url(r'^pricing/$', TemplateView.as_view(template_name='base.html'), name='home'),
    #url(r'^contact_us/$', TemplateView.as_view(template_name='pricing.html'), name='home'),
    url(r'^$', 'srvup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
