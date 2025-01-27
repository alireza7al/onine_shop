from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5, label='امتیاز (از ۱ تا ۵)')
