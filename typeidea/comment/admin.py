from django.contrib import admin
from .models import Comment
from typeidea.custom_site import custom_site


@admin.register(Comment,site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['target','nickname','content','website']
    fields = ['target','content','website','email','status']

    def save_model(self, request, obj, form, change):
        obj.nickname = request.user.username
        obj.save()



