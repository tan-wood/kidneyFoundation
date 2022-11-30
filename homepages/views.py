from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
import json
from homepages.models import Food, Nutrient

def indexPageView(request):
    return render(request,'homepages/index.html')

def LandingPageView(request):
    return render(request,'homepages/landingpage.html')

def LoginPageView(request):
    return render(request, 'homepages/login.html')

def AboutPageView(request):
    return render(request, 'homepages/about.html')
# def apiPageView(request) :
#     response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={settings.API_KEY}&query=Cheddar%20Cheese').json()
#     print(response)
#     return render(request,'homepages/apitest.html',{'response':response})


def apiJSONView(request) :
    response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query=apple&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=asc&api_key={settings.API_KEY}').json()
    return JsonResponse(response)


# also this will return the searched_food description (name) too
def apiPageView(request) :
    all_food_data = {}
    searched_food = {}
    food_nutrients = {}

    nutrientList = [
        'Protein',
        'Potassium, K',
        'Carbohydrate, by difference',
        'Sodium, Na',
        'Water',
        'Phosphorus, P',
    ]


    # maybe put in some logic for a blank search
    if 'name' in request.GET:
        if request.GET['name'] != '' :

            name = request.GET['name']
            response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={name}&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
            data = response.json()
            searched_food = data['foods'][0]

            
            
            # food_nutrients = searched_food['foodNutrients'][0]
            for nutrient in searched_food['foodNutrients'] :
                food_nutrients[ nutrient['nutrientName'] ] = [{ 'value' : nutrient['value']}, {'unitName' : nutrient['unitName']}]

                if nutrient['nutrientName'] in nutrientList :
                    nutrient_data = Nutrient(
                        # this will have some logic to decide if macro or micro
                        # alsooo it doesn't like it?
                        nutrient_name = nutrient['nutrientName'],
                    )

                    nutrient_data.save()




    

            food_data = Food(
                food_name = searched_food['description']

                # i don't need these?... weird!
                # food_group = 'dairy',
                # meal_category = 'breakfast',
            )

            # patient_logs_food_data = 
                # patient
                # food
                # time
                # measurement
                # quantity

            # nutrition_data = Nutrient(
            #     # this will have some logic to decide if macro or micro
            #     nutrient_is_macro = 'True'
            #     nutrient_name = searched_food

            # )

            # nutrient_in_food_data = 


            food_data.save()
            searched_food = Food.objects.all()

        


    # send it to the database when clicked!
    # not sure if that's in this view or not.. i think it is
    # food_name = WHAT BUTTON THEY CLICKED
    # something = Food.objects.something?


    return render (request, 'homepages/apitest.html', { "food_nutrients": 
    food_nutrients} )










###### THIS IS IF WE WANT OPTIONS #######
# def apiPageView(request) :
#     food_names = {}
#     global searchedFoods
#     # maybe put in some logic for a blank search
#     if 'name' in request.GET:
#         name = request.GET['name']
#         response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={name}&dataType=&pageSize=8&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
#         data = response.json()
#         searchedFoods = data['foods']
 
#         for idx, food in enumerate(searchedFoods) :
#             food_names['food_name' + str(idx+1)] = food['description']
    


#     # send it to the database when clicked!
#     # not sure if that's in this view or not.. i think it is
#     # food_name = WHAT BUTTON THEY CLICKED
#     # something = Food.objects.something?


#     return render (request, 'homepages/apitest.html', { "food_names": 
#     food_names} )


# def recordNutrientInfo() :
#     # food_info = {}
#     print('Hello')
#     food_data = Food(
#         food_name = searchedFoods[0]['description'],
#         food_group = 'dairy',
#         meal_category = 'breakfast',
#     )

#     food_data.save(update_fields='food_name')
    # food_info = Food.objects.all()




