from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Post
from django.contrib.auth.decorators import login_required


# Create your views here.
# 포스트 목록
def post_list(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'blogs/post_list.html', context)

# 포스트 상세
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    context = {
        'post': post
    }
    return render(request, 'blogs/post_detail.html', context)

# 포스트 글쓰기
@login_required
def post_write(request):
    errors = []
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')

        if not title:
            errors.append('제목을 입력하세요.')
        if not content:
            errors.append('내용을 입력하세요.')

        if not errors:
            post = Post.objects.create(user=request.user, title=title, content=content, image=image)

            return redirect('blogs:post_list')

    context = {
        'user': request.user,
        'errors': errors
    }
    return render(request, 'blogs/post_write.html', context)

