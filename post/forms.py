from django.forms import ModelForm
from cloudinary.forms import CloudinaryFileField
from .models import Post
from django.utils.translation import ugettext_lazy as _


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ('category', 'genre', 'tags', 'title', 'content', 'image', 'is_featured', 'is_entry',)
        labels = {
            'is_featured': _('Make this post public'),
            'is_entry': _('Enter this post in current competition'),
            'image-clear': _('')
        }
        help_texts = {
            'is_entry': _('Important! Copy your post before entering a competition; If you are not a subscriber or'
                          ' the entry period is over when you save, you will loose the post.')
        }
