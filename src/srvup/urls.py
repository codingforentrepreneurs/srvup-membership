from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    #url(r'^about/$', TemplateView.as_view(template_name='base.html'), name='home'),
    #url(r'^pricing/$', TemplateView.as_view(template_name='base.html'), name='home'),
    #url(r'^contact_us/$', TemplateView.as_view(template_name='pricing.html'), name='home'),
    url(r'^$', 'srvup.views.home', name='home'),
    url(r'^staff/$', 'srvup.views.staff_home', name='staff'),
    #url(r'^about/about/about/$', 'srvup.views.home', name='about'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^projects/$', 'videos.views.category_list', name='projects'),
    url(r'^projects/(?P<cat_slug>[\w-]+)/$', 'videos.views.category_detail', name='project_detail'),
    url(r'^projects/(?P<cat_slug>[\w-]+)/(?P<vid_slug>[\w-]+)/$', 'videos.views.video_detail', name='video_detail'),
    url(r'^admin/', include(admin.site.urls)),
)


#auth login/logout
urlpatterns += patterns('accounts.views',
	url(r'^logout/$', 'auth_logout', name='logout'),
    url(r'^login/$', 'auth_login', name='login'),
)



#Comment Thread
urlpatterns += patterns('comments.views',
    url(r'^comment/(?P<id>\d+)$', 'comment_thread', name='comment_thread'),
    url(r'^comment/create/$', 'comment_create_view', name='comment_create'),
)


#Notifications
urlpatterns += patterns('notifications.views',
    url(r'^notifications/$', 'all', name='notifications_all'),
    url(r'^notifications/unread/$', 'all', name='notifications_all'),
    url(r'^notifications/read/$', 'all', name='notifications_all'),
)



