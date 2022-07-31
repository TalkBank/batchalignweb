from django.contrib import admin
from .models import Job, Transcript, Audio, Fluency, Corpus

# Register your models here.
admin.site.register(Job)
admin.site.register(Transcript)
admin.site.register(Audio)
admin.site.register(Fluency)
admin.site.register(Corpus)

