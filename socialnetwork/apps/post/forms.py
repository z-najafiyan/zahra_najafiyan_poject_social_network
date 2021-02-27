from django import forms

from apps.post.models.post import Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'created_on', 'content', 'author', 'updated_on', 'status', 'picture']
