# 3rd part Imports
from django import forms
# Internal imports
from . models import Comment

# Registered user Comment form


class CommentForm(forms.ModelForm):
    """
    A form for registered users to leave comments on blog posts.
    """

    class Meta:
        model = Comment
        fields = ('body',)
