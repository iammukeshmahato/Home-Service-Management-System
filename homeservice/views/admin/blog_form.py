from django import forms
from homeservice.models import Blog
from ckeditor.widgets import CKEditorWidget


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": CKEditorWidget(),
        }
