from django.shortcuts import render
from .models import *

def index(request):
    return render(request, 'poster_app/index.html')
