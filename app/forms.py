# import forms
from django import forms

# import models
from .models import Corpus

# get a list of all corpuses
CORPUSES = Corpus.objects.all()
# and get a list of their names and keys
CORPUS_CHOICES = [(i.pk, i.name) for i in CORPUSES]

# submitting new audio file
class SubmissionForm(forms.Form):
    job_name = forms.CharField(label="Job name", max_length=200)
    submitter_name = forms.CharField(label="Submitter name", max_length=200)
    email = forms.EmailField(label="Submitter email")
    corpus = forms.ChoiceField(label="Corpus", choices=CORPUS_CHOICES)
    audio = forms.FileField(label="Audio file (.mp3/.wav)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set placeholders
        self.fields['job_name'].widget.attrs.update({'placeholder': "my experiment trial 3"})
        self.fields['submitter_name'].widget.attrs.update({'placeholder': "John Doe"})
        self.fields['email'].widget.attrs.update({'placeholder': "john@doe.edu"})


