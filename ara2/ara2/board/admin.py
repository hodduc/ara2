from django.contrib import admin
from ara2.board import models

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
