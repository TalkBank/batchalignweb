# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# index view to submit a job
def index(req):
    return render(req, "app/index.html", {})

