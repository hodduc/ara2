from rest_framework import serializers
from ara2.account.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups',
                  'nickname', 'signature', 'self_introduction', 'default_language',
                  'campus', 'widget', 'layout', 'last_logout_time', 'last_login_ip',
                  'is_sysop', 'authentication_mode', 'listing_mode', 'deleted')

