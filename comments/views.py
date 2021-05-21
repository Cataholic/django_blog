from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from .form import CommentForm
from blog.models import Post


# @require_POST
def comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(False)
        comment.post = post
        comment.save()
        messages.add_message(request, messages.SUCCESS, '评论成功！', extra_tags='success')
        return redirect(post)
    messages.add_message(request, messages.ERROR, '评论失败', extra_tags='danger')
    return render(request, 'comments/preview.html', context={'post':post, 'form':form})