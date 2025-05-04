from django.contrib import admin
from .models import *
from django import forms
from ckeditor.widgets import CKEditorWidget
import re


class RemoveLineHeightStyle(CKEditorWidget):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            value = self.remove_line_height_style(value)
        return super().render(name, value, attrs, renderer)

    def remove_line_height_style(self, text):
        cleaned_text = re.sub(r'line-height:\s*\d+(\.\d+)?;?', '', text)
        return cleaned_text


class PostAdminForm(forms.ModelForm):
    name = forms.CharField(required=False, max_length=255)
    text = forms.CharField(widget=CKEditorWidget(), required=False)

    def clean_content(self):
        print("clean content--------")

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Post, PostAdmin)
admin.site.register(ManageFalseModel)
admin.site.register(FileUploadModel)
