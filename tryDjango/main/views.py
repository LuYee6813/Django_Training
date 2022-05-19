from django.shortcuts import render
from django.http import HttpResponse
import random
# Create your views here.


def home(request):
    rand_num = randnum()
    content = {'randnum':rand_num}
    return render(request, 'home.html',content)

def randnum():
    num = random.randint(0,99)
    return num

