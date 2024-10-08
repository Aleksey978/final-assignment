from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


from .models import Post

class PostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
       ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }


