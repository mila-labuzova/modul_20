from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'author',
            'category',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        if name is not None and len(name) < 5:
            raise ValidationError({
                "name": "Название не может быть менее 5 символов."
            })

        text = cleaned_data.get("text")
        if text is not None and len(text) < 50:
            raise ValidationError({
                "text": "Содержание не может быть менее 50 символов."
            })

        return cleaned_data