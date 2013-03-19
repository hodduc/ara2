from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from ara2.account.views import UserList, UserDetail


urlpatterns = patterns('ara2.account.views',
    url(r'^$', 'api_root'),
    url(r'^users/$', UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>\d+)/$', UserDetail.as_view(), name='user-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

urlpatterns += patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)

