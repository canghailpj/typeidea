from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from .models import Link
from blog.views import CommonViewMixin

class LinkListView(CommonViewMixin,ListView):
    """友链视图"""
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'link_list'
