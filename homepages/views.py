from django.shortcuts import render
from django.http import HttpResponse

def indexPageView(request) :
    return render(request,'homepages/index.html')

def LandingPageView(request):
    return render(request,'landingpage.html')

def LoginPageView(request):
    return render(request, 'login.html')

def AboutPageView(request):
    return render(request, 'homepages/about.html')