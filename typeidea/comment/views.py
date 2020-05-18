from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from .forms import CommentForm


class CommentView(TemplateView):
    """评论视图"""
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        print('target......')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            successed = True
            # return redirect(target)
        else:
            successed = False

        context = {
            'successed': successed,
            'form': comment_form,
            'target': target,
        }
        return self.render_to_response(context)
