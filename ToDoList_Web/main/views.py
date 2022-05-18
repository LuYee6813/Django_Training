from django.shortcuts import render
from django.http import HttpResponse
from .models import ToDoList, Item

def index(request):
    return render(request, "base.html",{})
def home(request):
    return render(request,"home.html",{})
