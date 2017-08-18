from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('is_featured', 'is_entry', 'title', 'content', 'image', 'category', 'genre')