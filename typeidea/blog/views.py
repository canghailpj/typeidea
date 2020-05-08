from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from .models import Post, Tag, Category
from config.models import SideBar


def post_list(request, category_id=None, tag_id=None):
    """
    同一个视图中处理多个url逻辑
    :param request:
    :param category_id:
    :param tag_id:
    :return:
    """
    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all()
    }
    context.update(Category.get_navs())

    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id=None):
    try:
        post = Post.objects.get(id=post_id)  # get方法只能匹配一条记录，返回字典形式，filter返回一个queryset列表
    except:
        post = None

    context = {
        'post': post,
        'sidebars': SideBar.get_all()
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)


class PostListView(ListView):
    # queryset = Post.latest_posts()
    paginate_by = 1  # 设置每页条数
    # context_object_name = 'post_list'
    template_name = 'blog/detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = Post.latest_posts()
        context['sidebars'] = SideBar.get_all
        context.update(Category.get_navs())
        return context


######CBV代码重构

class CommonViewMixin:
    """
    通用视图：分类导航、侧边栏、底部导航
    """

    def get_context_data(self, **kwargs):
        """通过重写此方法，返回额外的数据"""
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all,
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    """首页视图"""
    queryset = Post.latest_posts()
    paginate_by = 1  # 设置每页5条数据
    context_object_name = 'post_list'  # 传给模板中的对象名称
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    """分类视图"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 获取公共视图中的sidebars数据
        category_id = self.kwargs.get('category_id')  # 获取请求中的参数
        category = get_object_or_404(Category, pk=category_id)
        print('分类',category)
        context.update({
            'category': category
        })
        return context

    def get_queryset(self):
        """重写queryset,根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    """分类视图"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # 获取公共视图中的sidebars数据
        tag_id = self.kwargs.get('tag_id')  # 获取请求中的参数
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写queryset,根据分类过滤"""
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag_id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
