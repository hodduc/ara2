from django.contrib import admin
from ara2.board import models


admin.site.register(models.Article)
admin.site.register(models.ArticleVoteStatus)
admin.site.register(models.BbsManager)
admin.site.register(models.Blacklist)
admin.site.register(models.Board)
admin.site.register(models.BoardHeading)
admin.site.register(models.BoardNotice)
admin.site.register(models.Category)
admin.site.register(models.File)
admin.site.register(models.ScrapStatus)
admin.site.register(models.SelectedBoard)
