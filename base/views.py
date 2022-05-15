from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    # return HttpResponse('Home Page')
    return render(request, 'home.html')

def room(request):
    # return HttpResponse('Room')
    return render(request, 'room.html')
