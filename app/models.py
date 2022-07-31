from django.db import models

# Create your models here.
from django.db import models

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
    # corpus to which the job belongs
    corpus_name = models.CharField(max_length=200)
    # name of the submitter
    submitter_name = models.CharField(max_length=200)
    # email of the submitter
    submitter_email = models.EmailField()
    # ENUM for the status of the job
    status = models.CharField(max_length=1, choices=STATE_CHOICES)

class Audio(models.Model):
    # Audio files submitted as a part of a job
    # when a job gets deleted, the audio file should go too
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    # the actual audio file
    file = models.FileField()

class Transcript(models.Model):
    # Chat files produced as a part of a job
    # when a job gets deleted, the audio file should go too
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    # the actual audio file
    file = models.FileField()

class Fluency(models.Model):
    # Flucalc XSLX files produced as a part of a job
    # when a job gets deleted, the audio file should go too
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)
    # the actual audio file
    file = models.FileField()

