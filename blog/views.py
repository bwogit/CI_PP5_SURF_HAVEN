# 3rd party Imports
from django.views import generic, View
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

# Internal:
from .models import Post
from .forms import CommentForm

# View for all published posts


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_date')
    template_name = 'blog.html'
    paginate_by = 2  # Corrected the typo here

    def get(self, request, *args, **kwargs):
        """
        This view renders the blog page and also all published posts
        """

        # Get all published posts
        posts = Post.objects.filter(status=1)
        # Paginate the posts
        paginator = Paginator(posts, 2)
        page = request.GET.get('page')
        postings = paginator.get_page(page)

        # Render the blog page with the paginated posts
        return render(
            request, 'blog/blog.html',  {'posts': posts, 'postings': postings}
        )

# View for the post to be read by the user


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        """
        This view renders the blog post detail page
        """

        # Get the post with the given slug
        post = get_object_or_404(Post.objects.filter(status=1), slug=slug)
        # Get all approved comments for the post
        comments = post.comments.filter(approved=True)
        comments = comments.order_by('-created_date')

        # Render the blog post detail page with the post and comments
        return render(
            request, 'blog/blog_detail.html',
            {'post': post,
             'comments': comments,
             'commented': False,
             'comment_form': CommentForm()
             }
        )

    def post(self, request, slug, *args, **kwargs):
        """
        This view handles post requests to the blog post detail page
        """

        # Get the post with the given slug
        post = get_object_or_404(
            Post.objects.filter(status=1),
            slug=slug
        )

        # Get all approved comments for the post
        comments = post.comments.filter(approved=True)
        comments = comments.order_by('-created_date')

        # Create a comment form instance from the request POST data
        comment_form = CommentForm(data=request.POST)

        # Try to save the comment form
        try:
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Comment pending approval')
        except Exception as e:
            messages.error(request, 'Please try again')

        # Render the blog post detail page with the post, comments, and form
        return render(
            request, 'blog/blog_detail.html',
            {'post': post,
             'comments': comments,
             'commented': True,
             'comment_form': CommentForm()
             }
        )
