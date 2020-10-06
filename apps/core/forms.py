from django import forms
from .models import Video


class FileForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ["video"]


class GeneratorForm(forms.Form):
    threshold = forms.IntegerField()
    limit = forms.IntegerField()
