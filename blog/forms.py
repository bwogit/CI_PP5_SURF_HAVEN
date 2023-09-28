# Imports
from django import forms
# Internal:
from . models import Comment

# Registered user Comment form 


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
