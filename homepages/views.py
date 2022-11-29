from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
import json

def indexPageView(request) :
    return render(request,'homepages/index.html')


# def apiPageView(request) :
#     response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={settings.API_KEY}&query=Cheddar%20Cheese').json()
#     print(response)
#     return render(request,'homepages/apitest.html',{'response':response})


def apiJSONView(request) :
    response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query=apple&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=asc&api_key={settings.API_KEY}').json()
    return JsonResponse(response)

def apiPageView(request) :
    food_names = {}
    if 'name' in request.GET:
        name = request.GET['name']
        response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={name}&dataType=&pageSize=8&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
        data = response.json()
 
        for idx, food in enumerate(data['foods']) :
            food_names['food_name' + str(idx+1)] = food['description']
    

    # send it to the database when clicked!
    # not sure if that's in this view or not.. i think it is
    # food_name = WHAT BUTTON THEY CLICKED
    # something = Food.objects.something?


    return render (request, 'homepages/apitest.html', { "food_names": 
    food_names} )

