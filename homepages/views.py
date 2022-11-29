from django.shortcuts import render
from django.http import HttpResponse
import requests

def indexPageView(request) :
    return render(request,'homepages/index.html')



# # Create your views here.
# def index(request):
#     response=requests.get('https://api.covid19api.com/countries').json()
#     return render(request,'index.html',{'response':response})