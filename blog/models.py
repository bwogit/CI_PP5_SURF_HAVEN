# Imports
from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, 'Draft'), (1, 'Posted'))


# Post model
class Post(models.Model):
    """
    A blog post.
    """

    post_id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=200,
        unique=True
        )
    slug = models.SlugField(
        max_length=200,
        unique=True
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
        )
    created_date = models.DateTimeField(auto_now_add=True)  # set on creation
    updated_date = models.DateTimeField(auto_now=True)  # update on every save
    content = models.TextField()
    featured_image = models.ImageField(
        null=True,
        blank=True
        )
    excerpt = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()


# Comment model

class Comment(models.Model):
    """
    A comment on a blog post.

    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
        )
    name = models.CharField(
        max_length=50
        )
    email = models.EmailField()
    body = models.TextField()
    created_date = models.DateTimeField(
        auto_now_add=True
        )
    approved = models.BooleanField(
        default=False
        )

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'Comment {self.body} by {self.name}'
