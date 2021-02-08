from django.contrib import admin
from . import models
from .models import Hall, User, Show, People, Review, Feed_post, Feed_comment, Time, Profile


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username",)


admin.site.register(Hall)
admin.site.register(Show)
admin.site.register(People)
admin.site.register(Review)
admin.site.register(Feed_post)
admin.site.register(Feed_comment)
admin.site.register(Time)
admin.site.register(Profile)