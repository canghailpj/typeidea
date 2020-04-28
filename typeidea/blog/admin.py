from django.contrib import admin
from .models import Category,Post,Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','status','owner','created_time','is_nav')
    fields = ('name','status','is_nav','owner')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        # return super(CategoryAdmin,self).save_model(request,obj,form,change)
        obj.save()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','owner','status','created_time')
    fields = ('name','status')


    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        # return super(CategoryAdmin,self).save_model(request,obj,form,change)
        obj.save()

# admin.site.register(Category,CategoryAdmin)

