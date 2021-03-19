from django import forms
from django.core.exceptions import ValidationError

from apps.post.models import Comment
from apps.post.models.post import Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'created_on', 'content', 'updated_on', 'status', 'picture']

    def clean(self):
        cleaned_data = super().clean()
        picture = cleaned_data.get('picture')
        content = cleaned_data.get('content')
        if picture == None and content == None:
            raise ValidationError("Enter a picture or content")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    # def form_valid(self, form):
    #     form.instance.post_id = self.kwargs.get('pk')
    #     form.instance.user_id = self.kwargs.get('pk')
    #     return super(CommentForm, self).form_valid(form)
