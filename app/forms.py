# import forms
from django import forms

# import models
from .models import Corpus

# submitting new audio file
class SubmissionForm(forms.Form):
    name = forms.CharField(label="Job name", max_length=200, required=True)
    submitter_name = forms.CharField(label="Submitter name", max_length=200, required=True)
    submitter_email = forms.EmailField(label="Submitter email", required=True)
    corpus = forms.ModelChoiceField(label="Corpus", queryset=Corpus.objects.all(), required=True)
    audio = forms.FileField(label="Audio file (.mp3/.wav)", required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set placeholders
        self.fields['name'].widget.attrs.update({'placeholder': "my experiment trial 3"})
        self.fields['submitter_name'].widget.attrs.update({'placeholder': "John Doe"})
        self.fields['submitter_email'].widget.attrs.update({'placeholder': "john@doe.edu"})


