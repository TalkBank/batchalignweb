# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# import our forms
from .forms import SubmissionForm

# and import our models for Job
from .models import Job, Audio

# index view to submit a job
def submit(req):
    # create and render submission form
    form = SubmissionForm()
    return render(req, "app/submit.html", {'form': form})

def handle_job_submission(req):
    # recreate the submitted form
    form = SubmissionForm(req.POST, req.FILES)
    # if not valid, return
    if not form.is_valid():
        return
    # serialize form result into object
    job = Job(**form.cleaned_data)
    job.save()
    # and serialize the audio
    audio = Audio(job=job, file=form.cleaned_data["audio"])
    audio.save()
    # return UUID
    return job.job_id

# index view to submit a job
def jobs(req, job_id=None):
    # handle submission
    if req.method == 'POST':
        # if we are submitting a new job, we submit it 
        new_uuid = handle_job_submission(req)
        # if we have validated
        if new_uuid:
            # redirect!
            return HttpResponseRedirect(f"/jobs/{str(new_uuid)}")
        else:
            # redirect!
            return HttpResponseRedirect(f"/")

    return HttpResponse("hewo")



# import asyncio
# from django.http import JsonResponse
# from asgiref.sync import sync_to_async
# from time import sleep

# @sync_to_async
# def crunching_stuff():
#     sleep(10)
#     print("Woke up after 10 seconds!")

# async def index(request):
#     json_payload = {
#         "message": "Hello world"
#     }
#     """
#     or also
#     asyncio.ensure_future(crunching_stuff())
#     loop.create_task(crunching_stuff())
#     """
#     asyncio.create_task(crunching_stuff())
#     return JsonResponse(json_payload)
