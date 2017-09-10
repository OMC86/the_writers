from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('category', 'genre', 'title', 'content', 'image', 'is_featured', 'is_entry',)
