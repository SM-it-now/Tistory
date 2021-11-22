from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


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

    # 좋아요 디폴트
    is_liked = False

    # 좋아요 토글
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'total_likes': post.total_likes()
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

# 좋아요 기능
@login_required
@require_POST
def post_like(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = post.likes.filter(id=request.user.id).exists()

    # 좋아요 토글 기능 구현
    if is_liked:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(reverse('blogs:post_detail', kwargs={'post_id': post.id}))





