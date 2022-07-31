# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# import our forms
from .forms import SubmissionForm

# index view to submit a job
def submit(req):
    form = SubmissionForm()
    return render(req, "app/submit.html", {'form': form})

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
