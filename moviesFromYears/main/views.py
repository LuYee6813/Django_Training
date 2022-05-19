from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Movie
# Create your views here.

def movies(request):
    data = Movie.objects.all()
    return render(request,'movies.html',{'movies':data})

def detail(request, id):
    data = Movie.objects.get(pk=id)
    return render(request,'detail.html',{'movie':data})

def add(request):
    title = request.POST.get('title')
    year = request.POST.get('year')
    if title and year:
        movie = Movie(title=title, year=year)
        movie.save()
        return HttpResponseRedirect('/')   
    return render(request, 'add.html',{'title':title,'year':year})