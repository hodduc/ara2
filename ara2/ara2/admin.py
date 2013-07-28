from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, AdminPasswordChangeForm
from django.utils.translation import ugettext_lazy as _

from ara2 import models

class LostPasswordTokenAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )

class UserActivationAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )

class MessageAdmin(admin.ModelAdmin):
    raw_id_fields = ('from_user', 'to_user')

admin.site.register(models.LostPasswordToken, LostPasswordTokenAdmin)
admin.site.register(models.UserActivation, UserActivationAdmin)
admin.site.register(models.Message, MessageAdmin)


class UserChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password = ReadOnlyPasswordHashField(label=_("Password"),
                                         help_text=_("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = models.User

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class AraUserAdmin(UserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('nickname', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Ara profile'), {'fields': ('signature',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'nickname', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'nickname', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

# Re-register UserAdmin
admin.site.register(models.User, AraUserAdmin)

class ArticleAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', 'root', 'parent')

class ArticleVoteStatusAdmin(admin.ModelAdmin):
    raw_id_fields = ('article', 'user')

class BbsManagerAdmin(admin.ModelAdmin):
    raw_id_fields = ('manager', )

class BlacklistAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'blacklisted_user')

class BoardNoticeAdmin(admin.ModelAdmin):
    raw_id_fields = ('article', )

class FileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'article')

class ScrapStatusAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'article')

class SelectedBoardAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )

admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleVoteStatus, ArticleVoteStatusAdmin)
admin.site.register(models.BbsManager, BbsManagerAdmin)
admin.site.register(models.Blacklist, BlacklistAdmin)
admin.site.register(models.Board)
admin.site.register(models.BoardHeading)
admin.site.register(models.BoardNotice, BoardNoticeAdmin)
admin.site.register(models.Category)
admin.site.register(models.File, FileAdmin)
admin.site.register(models.ScrapStatus, ScrapStatusAdmin)
admin.site.register(models.SelectedBoard, SelectedBoardAdmin)


admin.site.register(models.Banner)
admin.site.register(models.Visitor)
