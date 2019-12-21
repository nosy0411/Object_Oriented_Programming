from .models import Post
from django import forms


class PostForm(forms.ModelForm):
    content = forms.CharField(label="글 내용")
    class Meta:
        model = Post
        fields = ('content',)
