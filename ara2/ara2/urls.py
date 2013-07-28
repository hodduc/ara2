from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from ara2.views.account import UserList, UserDetail

admin.autodiscover()

account = patterns('ara2.views.account',
    url(r'^$', 'api_root'),
    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>\d+)/$', UserDetail.as_view(), name='user-detail'),
)

account = format_suffix_patterns(account, allowed=['json', 'api'])

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ara2.views.home', name='home'),
    # url(r'^ara2/', include('ara2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^account/', include(account)),
)

