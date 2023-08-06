import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.utils.text import slugify
from django.utils import timezone

from .models import Post, Upvote
from .mixins import AuthorRequiredMixin
from .settings import settings as app_settings

common_context = {
    'settings': app_settings
}


class BlogHomeView(View):
    
    def get(self, request):
        posts_list = Post.objects.filter(is_deleted=False, is_published=True)
        paginator = Paginator(posts_list, 15)

        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, 'django-blogs/home.html', {
            'posts': posts,
            **common_context,
        })

class NewBlogView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request):
        post = Post.objects.create(
            author=request.user.username,
            uuid=uuid.uuid4(),
            heading="",
            content=""
        )
        return redirect('blogs:edit', uuid=post.uuid)

class BlogEditView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request, uuid):
        post = get_object_or_404(Post, pk=uuid)
        if not post.author == request.user.username:
            raise PermissionDenied
        return render(request, 'django-blogs/editor.html', {
            'blog': post,
            **common_context,
        })
    
    def post(self, request, uuid):
        if not all([key in request.POST for key in ['heading', 'content']]):
            return JsonResponse(
                {
                    'error': "'heading' and 'content' required"
                },
                status=400)
        post = get_object_or_404(Post, pk=uuid)
        if not post.author == request.user.username:
            raise PermissionDenied
        post.heading = request.POST['heading']
        post.slug = '-'.join([
            slugify(request.POST['heading'])[:200],
            post.uuid.hex[:12]
        ])
        post.content = request.POST['content']
        post.save()
        return HttpResponse(status=200)

class BlogDraftView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request):
        posts_list = Post.objects.filter(
            author__exact=request.user.username,
            is_deleted=False,
            is_published=False)
        paginator = Paginator(posts_list, 15)

        page = request.GET.get('page')
        posts = paginator.get_page(page)
        return render(request, 'django-blogs/drafts.html', {
            'posts': posts,
            **common_context,
        })

class BlogReadView(View):

    def get(self, request, slug):
        post = get_object_or_404(
            Post,
            slug=slug,
            is_deleted=False,
            is_published=True)
        upvote_count = post.upvote_set.filter(is_upvoted=True).count()
        return render(request, 'django-blogs/blog.html', {
            'post': post,
            'upvote_count': upvote_count,
            **common_context
        })

class BlogPublishView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request, uuid):
        post = get_object_or_404(Post, pk=uuid)
        if not post.author == request.user.username:
            raise PermissionDenied
        post.is_published = True
        post.published_on = timezone.now()
        post.slug = '-'.join([
            slugify(post.heading)[:200],
            post.uuid.hex[:12]
        ])
        post.save()
        return redirect("blogs:read", slug=post.slug)

class BlogDeleteView(LoginRequiredMixin, AuthorRequiredMixin, View):

    def get(self, request, uuid):
        post = get_object_or_404(Post, pk=uuid)
        if not post.author == request.user.username:
            raise PermissionDenied
        post.is_deleted = True
        post.save()
        return redirect("blogs:home")

class UpvoteView(View):

    def get(self, request, uuid):
        data = request.GET
        if not data.get('fingerprint', ''):
            return HttpResponse(status=400)
        upvote, created = Upvote.objects.get_or_create(
            post_id=uuid,
            fingerprint=data['fingerprint']
        )
        return JsonResponse(
            {
            'is_upvoted': upvote.is_upvoted
            },
            status=200
        )

    def post(self, request, uuid):
        data = request.POST
        if not data.get('fingerprint', ''):
            return HttpResponse(status=400)
        upvote, created = Upvote.objects.get_or_create(
            post_id=uuid,
            fingerprint=data['fingerprint']
        )
        upvote.is_upvoted = not upvote.is_upvoted
        upvote.save()
        return HttpResponse(status=200)