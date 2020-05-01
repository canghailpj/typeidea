from django.contrib import admin
from django.urls import reverse
from .models import Category,Post,Tag
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','status','owner','created_time','is_nav')
    fields = ('name','status','is_nav')

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


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    文章列表右侧过滤器：只显示自己创建的分类
    """

    title = '分类过滤器'
    parameter_name = 'owner_category'   #过滤时url中传的参数名称

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)

        return queryset


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

    list_display = ['title','category','owner','status',
                    'created_time',]
    list_display_links = ['title']
    # list_filter = ['category']
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title','category']
    # actions_on_bottom = True
    actions_on_top = True


    #编辑页面
    save_on_top = True

    # exclude = ('owner',)
    #
    # fields = (
    #     ('category','title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ('基础配置',{
            'description':'下列是基础配置项',
            'fields':(
                ('title','category'),
                'status',
            )
        }),
        ('内容',{
            'fields':(
                'desc',
                'content',
            ),
        }),
        ('额外信息',{
            'classes':('collage',),
            'fields':('tag',),
        })
    )

    filter_horizontal = ('tag',)   #多对多字段横向展示
    # filter_vertical = ('tag',)   #多对多字段纵向展示



    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()
        return qs.filter(owner=request.user)

    #引入自定义资源
    class Media:
        css = {}
        js = {}

# admin.site.register(Category,CategoryAdmin)

