from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry
from .models import Category, Post, Tag
from .adminforms import PostAdminForm
from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    """
    记录所有model的操作日志
    """
    list_display = ('object_repr', 'object_id', 'action_flag', 'user', 'change_message')


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 3  # 默认显添加文章的个数
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline]  # 在分类页面直接编辑文章
    list_display = ('name', 'status', 'owner', 'created_time', 'is_nav')
    fields = ('name', 'status', 'is_nav')


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'owner', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """
    文章列表右侧过滤器：只显示自己创建的分类
    """

    title = '分类过滤器'
    parameter_name = 'owner_category'  # 过滤时url中传的参数名称

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)

        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm

    def operator(self, obj):
        # # a = reverse('admin:blog_post_change',args=(obj.id))
        #
        # return format_html('<a href="/index">编辑</a>')

        return format_html(
            '<a href="{}">编辑</a>',
            # reverse('blog_Post_change',args=(obj.id))
            # reverse('blog_Post_changelist')
            reverse('blog_Post_add')  # 反向url解析

        )

    operator.short_description = '操作'

    list_display = ['title', 'category', 'owner', 'status',
                    'created_time', ]
    list_display_links = ['title']
    # list_filter = ['category']
    list_filter = [CategoryOwnerFilter]
    search_fields = ['title', 'category']
    # actions_on_bottom = True
    actions_on_top = True

    # 编辑页面
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
        ('基础配置', {
            'description': '下列是基础配置项',
            'fields': (
                ('title', 'category'),
                'status',
            )
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collage',),
            'fields': ('tag',),
        })
    )

    filter_horizontal = ('tag',)  # 多对多字段横向展示

    # filter_vertical = ('tag',)   #多对多字段纵向展示

    # 引入自定义资源
    class Media:
        css = {}
        js = {}

# admin.site.register(Category,CategoryAdmin)
