from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1、用来自动补充文章、分类、标签、侧边栏、友链这些model的owner字段
    2、用来针对queryset过滤当前用户的数据
    """

    exclude = ('owner',)

    def get_queryset(self, request):
        qs = self.model._default_manager.get_queryset()
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()