from django.contrib import admin

from blogs.models import Post, Author, Upvote

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('uuid', 'heading', 'is_published')
    list_filter = ('is_published', 'is_deleted')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    list_display = ('user', 'is_author')
    list_filter = ('is_author', )

@admin.register(Upvote)
class UpvoteAdmin(admin.ModelAdmin):

    list_display = ('post', 'fingerprint', 'is_upvoted')