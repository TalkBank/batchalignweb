from django.db import models
from functools import partial

# Create your models here.
from django.db import models

class Corpus(models.Model):
    # ID of the job
    corpus_id = models.UUIDField()
    # A collection of jobs
    name = models.CharField(max_length=200)
    # Maintainer
    submitter_email = models.EmailField()

class Job(models.Model):
    # Serialize enums for job states
    SUCCESS = 'S'
    FAIL = 'F'
    PROCESSING = 'P'
    # create the state choices translation
    STATE_CHOICES = [
        (SUCCESS, 'Success'),
        (FAIL, 'Fail'),
        (PROCESSING, 'Processing'),
    ]

    # ID of the job
    job_id = models.UUIDField()
    # corpus to which the job belongs, deletes all job of corpus is deleted
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, null=True)
    # name of the submitter
    submitter_name = models.CharField(max_length=200)
    # email of the submitter
    submitter_email = models.EmailField()
    # ENUM for the status of the job
    status = models.CharField(max_length=1, choices=STATE_CHOICES, default=PROCESSING)

def file_path(instance, path=""):
    """Return the path to upload

    Attributes:
        instance (models.Model): model instance
        path (str): type of model (i.e. subdirectory)
    """

    return f"{path}/{instance.job.corpus.name}" if instance.job.corpus else f"{path}/"

class Audio(models.Model):
    # Audio files submitted as a part of a job
    # when a job gets deleted, the audio file should go too
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    # the actual audio file (upload to corpus folder if existing)
    file = models.FileField(upload_to=partial(file_path, "audio"))

class Transcript(models.Model):
    # Chat files produced as a part of a job
    # when a job gets deleted, the audio file should go too
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    # the actual transcript file
    file = models.FileField(upload_to=partial(file_path, "transcript"))

class Fluency(models.Model):
    # Flucalc XSLX files produced as a part of a job
    # when a job gets deleted, the audio file should go too
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    # the actual fluency file
    file = models.FileField(upload_to=partial(file_path, "fluency"))
    
