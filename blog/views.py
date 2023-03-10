from django.shortcuts import render, get_object_or_404
from blog.models import Comment, Post, Tag
from django.db.models import Count, Prefetch


def serialize_post(post):
    tags = post.post_tags
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_amount,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': tags,
        'first_tag_title': tags[0].title,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.posts_amount
    }


def index(request):
    most_popular_posts = Post.objects.popular().fetch_with_author_and_tags(
    )[:5].fetch_with_comments_count()

    most_fresh_posts = Post.objects.annotate(
        comments_amount=Count('comments')
    ).prefetch_related(
        Prefetch('author'),
        Prefetch('tags', queryset=Tag.objects.popular(), to_attr='post_tags')
    ).order_by('-published_at')[:5]

    most_popular_tags = Tag.objects.popular()[:5]

    context = {
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
        'page_posts': [
            serialize_post(post) for post in most_fresh_posts
        ],
        'popular_tags': [
            serialize_tag(tag) for tag in most_popular_tags
        ],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post_query_set = Post.objects.annotate(
        likes_amount=Count('likes')
    ).select_related('author')
    post = get_object_or_404(post_query_set, slug=slug)
    comments = Comment.objects.filter(post=post).select_related('author')
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        })

    related_tags = post.tags.all().popular()

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': comments,
        'likes_amount': post.likes_amount,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in related_tags],
    }

    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = Post.objects.popular().fetch_with_author_and_tags(
    )[:5].fetch_with_comments_count()

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = get_object_or_404(Tag, title=tag_title)

    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = Post.objects.popular().fetch_with_author_and_tags(
    )[:5].fetch_with_comments_count()

    related_posts = Post.objects.filter(tags=tag).prefetch_related(
        Prefetch('author'),
        Prefetch(
            'tags',
            queryset=Tag.objects.filter(title=tag_title),
            to_attr='post_tags'
        )
    )[:20].fetch_with_comments_count()

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # ?????????? ?????????? ?????????? ?????? ?????? ???????????????????? ?????????????? ???? ?????? ????????????????
    # ?? ?????? ???????????? ??????????????
    return render(request, 'contacts.html', {})