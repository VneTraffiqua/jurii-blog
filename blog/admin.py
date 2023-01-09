from django.contrib import admin
from blog.models import Post, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'published_at', 'author'
    )
    raw_id_fields = ('likes', 'tags')


admin.site.register(Tag)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post', 'author', 'published_at'
    )
    raw_id_fields = (
        'author',
    )
