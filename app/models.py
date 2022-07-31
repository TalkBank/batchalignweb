from django.db import models
from functools import partial
import uuid
import time

# Create your models here.
from django.db import models

class Corpus(models.Model):
    # better plural
    class Meta:
        verbose_name_plural = "Corpuses"

    # ID of the job
    corpus_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # A collection of jobs
    name = models.CharField(max_length=200)
    # Maintainer
    maintainer_email = models.EmailField()

    # string representation
    def __str__(self):
        return f"{self.name}"

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
    job_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # corpus to which the job belongs, deletes all job of corpus is deleted
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, null=True)
    # Name of the job
    name = models.CharField(max_length=200)
    # name of the submitter
    submitter_name = models.CharField(max_length=200)
    # email of the submitter
    submitter_email = models.EmailField()
    # ENUM for the status of the job
    status = models.CharField(max_length=1, choices=STATE_CHOICES, default=PROCESSING)

    # string representation
    def __str__(self):
        return f"Job {self.job_id}" + (" for " + self.corpus.name) if self.corpus else ""


def file_path(instance, file_name):
    """Return the path to upload

    Attributes:
        instance (models.Model): model instance
        file_name (str): name of the file
    """

    return f"{instance.job.job_id}/in/{file_name}"

class Audio(models.Model):
    # Audio files submitted as a part of a job
    # when a job gets deleted, the audio file should go too
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    # the actual audio file (upload to corpus folder if existing)
    file = models.FileField(upload_to=file_path)

    # string representation
    def __str__(self):
        return f"Audio {self.file.name}"

class Transcript(models.Model):
    # Chat files produced as a part of a job
    # when a job gets deleted, the audio file should go too
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    # the actual transcript file
    file = models.FileField(upload_to=file_path)

    # string representation
    def __str__(self):
        return f"Transcript {self.file.name}"

class Fluency(models.Model):
    # better plural
    class Meta:
        verbose_name_plural = "Fluencies"

    # Flucalc XSLX files produced as a part of a job
    # when a job gets deleted, the audio file should go too
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    # the actual fluency file
    file = models.FileField(upload_to=file_path)
    
    # string representation
    def __str__(self):
        return f"FluCalc {self.file.name}"


