from django.contrib import admin
from django.urls import reverse
from .models import Category,Post,Tag
from django.utils.html import format_html

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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    def operator(self,obj):
        # # a = reverse('admin:blog_post_change',args=(obj.id))
        #
        # return format_html('<a href="/index">编辑</a>')

        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('blog_Post_change',args=(obj.id))
            # reverse('blog_Post_changelist')
            reverse('blog_Post_add') #反向url解析

        )
    operator.short_description = '操作'

    list_display = ['title','category','status',
                    'created_time','tag',]
    list_display_links = ['tag']

    list_filter = ['category']
    search_fields = ['title','category']

    # actions_on_bottom = True
    actions_on_top = True


    #编辑页面
    save_on_top = True

    fields = (
        ('category','title'),
        'desc',
        'status',
        'content',
        'tag',
    )



    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

# admin.site.register(Category,CategoryAdmin)

