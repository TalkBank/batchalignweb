# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# import our forms
from .forms import SubmissionForm

# and import our models for Job
from .models import Job, Audio, Transcript

# async utilities
import asyncio
from asgiref.sync import sync_to_async
# threading utilities
from threading import Thread

# import batchalign
from .batchalign.ba.fa import do_align
from .batchalign.ba.utils import cleanup, globase
from .batchalign.ba.retokenize import retokenize_directory
# getting keys, variables, etc.
from django.conf import settings 

# static pages
from django.templatetags.static import static

# pathing utils
import os

# global worker
WORKER = asyncio.new_event_loop()

# function to run the event loop
def f(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

# start the worker loop on a different thread
t = Thread(target=f, args=(WORKER,), daemon=True)
t.start()

# async function to run job
async def run_job(job):
    print("HWEOOOOOO")
    # get tokenization model
    model = settings.TOKENIZATION_MODEL
    model_path = f'app/static/app/models/{model}/'
    # get the path to media
    media_path = settings.MEDIA_ROOT
    # get the API key
    key = settings.REV_API_KEY

    # get job id
    id = str(job.job_id)

    # get or create the i/o directories
    in_dir = os.path.join(media_path, id, "in")
    out_dir = os.path.join(media_path, id, "out")
    # make out directory
    os.mkdir(out_dir)

    # retokenize the directory!
    retokenize_directory(in_dir, model_path, False, key)

    # and then, run MFA!
    do_align(in_dir, out_dir, "data", prealigned=True, beam=200, align=True, clean=True)
    
    # find the output
    out_file = globase(out_dir, "*.cha")

    # if the length is <1, we failed
    # TODO check reason
    if len(out_file) < 1:
        job.status = Job.FAIL
        job.save()
    # otherwise, we have succeded, so let's get the file
    else:
        transcript = Transcript(job=job)
        transcript.file.name = out_file[0]
        transcript.save()

    # and done!

# function handle job submission
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
    # start the job running
    # WORKER.call_soon_threadsafe(asyncio.async, run_job(job))
    future = asyncio.run_coroutine_threadsafe(run_job(job), WORKER)
    # return UUID
    return job.job_id

# index view to submit a job
def submit(req):
    # create and render submission form
    form = SubmissionForm()
    return render(req, "app/submit.html", {'form': form})

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
