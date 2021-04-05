from django import forms

from apps.post.models import Comment
from apps.post.models.post import Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'created_on', 'content', 'updated_on', 'status', 'picture']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    # def form_valid(self, form):
    #     form.instance.post_id = self.kwargs.get('pk')
    #     form.instance.user_id = self.kwargs.get('pk')
    #     return super(CommentForm, self).form_valid(form)
