from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from ara2.account import models


admin.site.register(models.LostPasswordToken)
admin.site.register(models.UserActivation)
admin.site.register(models.Profile)
admin.site.register(models.Message)


class ProfileInline(admin.StackedInline):
    model = models.Profile
    can_delete = False


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)