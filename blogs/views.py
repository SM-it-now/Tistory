from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Post, Comment
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
    comments = Comment.objects.filter(post=post_id)

    context = {
        'post': post,
        'comments': comments
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

            return redirect(reverse('blog:post_detail', kwargs={'post_id': post.id}))

    context = {
        'user': request.user,
        'errors': errors
    }
    return render(request, 'blogs/post_write.html', context)


# 댓글 쓰기
@login_required
def comment_write(request):
    errors = []
    if request.method == 'POST':
        post_id = request.POST.get('post_id', '').strip()
        content = request.POST.get('content', '').strip()

        if not content:
            errors.append('댓글을 입력해주세요.')

        if not errors:
            comment = Comment.objects.create(user=request.user, post_id=post_id, content=content)

            return redirect(reverse('blogs:post_detail', kwargs={'post_id': comment.post.id}))

    context = {
        'user': request.user,
        'errors': errors
    }

    return render(request, 'blogs/post_detail.html', context)




