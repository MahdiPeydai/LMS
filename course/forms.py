from django import forms
from .models import Review
from ckeditor.fields import CKEditorWidget


class ReviewForm(forms.ModelForm):
    message = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Review
        fields = ['message']
