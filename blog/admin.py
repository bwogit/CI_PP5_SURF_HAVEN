# 3rd party Imports
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
# Internal imports
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content')
    list_filter = ('status', 'created_date')
    list_display = ('title', 'slug', 'status', 'created_date')
    search_fields = ['title', 'content']


# Registration of the comment items for the admin panel,
# display, search filters and actions
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_filter = ('approved', 'created_date')
    list_display = ('name', 'body', 'post', 'created_date', 'approved')
    search_fields = ['name', 'email', 'body']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
