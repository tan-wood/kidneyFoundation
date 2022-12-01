from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
import json
from homepages.models import Food, Nutrient, Patient, Alert, Nutrient_In_Food, Patient_Logs_Food, Measurement, Patient_Condition
from datetime import datetime as dt

loggedIn = False
loggedInUsername = ""
loggedInPatientId = None

def indexPageView(request):
    global loggedInPatientId
    if loggedInPatientId != None:
        data = Nutrient_In_Food.objects.all()
        patientData = Patient.objects.get(id = loggedInPatientId)
        nutrientNames = Nutrient.objects.all()
        current_date = dt.now().date()
        formatted_date = f'{current_date.strftime("%b")} {current_date.strftime("%d")}, {current_date.strftime("%Y")}'

        context = {
            'data':data,
            'patientData' : patientData,
            'nutrients' : nutrientNames,
            'formatted_date' : formatted_date
        }

    if loggedIn:
        return render(request,'homepages/index.html', context)
    else:
        return LandingPageView(request)

def SignOutPageView(request):
    global loggedIn
    global loggedInPatientId
    loggedIn = False
    loggedInPatientId = None
    return LandingPageView(request)

def AlertsPageView(request):
    global loggedInUsername
    
    if loggedIn:
        data = Alert.objects.all()
        user_alerts = []
        for alert in data:
            if alert.patient.username == loggedInUsername:
                user_alerts.append(alert)
        
        context = {
            "alerts": user_alerts
        }

        return render(request,'homepages/alerts.html', context)
    else:
        return LandingPageView(request)
    

def DiaryPageView(request):
    if loggedIn:
        food_data = Patient_Logs_Food.objects.all()
        nutrient_data = Nutrient_In_Food.objects.all()

        user_today_foods = []
        user_past_foods = []

        for food in food_data:
            if food.patient.username == loggedInUsername:
                food_object = {
                    'food': food,
                    'nutrients' : []
                }
                # Nutrients
                nutrient_list = []
                num_servings = food.quantity
                for nutrient in nutrient_data:
                    if nutrient.food.food_name == food.food.food_name:
                        nutrient_object = {
                            'name': nutrient.nutrient.nutrient_name,
                            'amount': round(nutrient.amount * num_servings, 2),
                            'measurement': nutrient.measurement.description
                        }
                        nutrient_list.append(nutrient_object)

                food_object['nutrients'] = nutrient_list

                if food.date_time.date() == dt.today().date():
                    user_today_foods.append(food_object)
                else:
                    user_past_foods.append(food_object)

        context = {
            "today_foods" : user_today_foods,
            "past_foods" : user_past_foods
        }

        return render(request,'homepages/diary.html', context)
    else:
        return LandingPageView(request)

def AccountPageView(request, method):
    if loggedInPatientId != None:
        patientData = Patient.objects.get(id = loggedInPatientId)
        
        if method == "homeAccount":
            context = {
                'patientData' : patientData,
                'display': "homeAccount",
            }
        elif method == "editPatient":
            context = {
                'patientData' : patientData,
                'display': "editPatient",
            }
        else:
            context = {
                'patientData' : patientData,
                'display': "changeLoginInfo",
            }
    if loggedIn:
        return render(request,'homepages/account.html', context)
    else:
        return LandingPageView(request)

def LandingPageView(request):
    global loggedIn
    if not loggedIn:
        context = {
            "signedIn": False
        }
    else:
        context = {
            "signedIn": True
        }
    return render(request,'homepages/landingpage.html', context)


def LoginPageView(request, method):
    global loggedIn
    global loggedInPatientId
    global loggedInUsername
    if request.method == 'POST' and method == "form":
        email = request.POST['email']
        username = request.POST['username']
        errors = ""

        data = Patient.objects.all()

        for patient in data:
            if email == patient.email:
                errors += "This email has already been registered <br>"
            if username == patient.username:
                errors += "This username is already taken <br>"
        if errors != "":
            context = {
                    "display" : "create",
                    "errors" : errors
                }
            return render(request, 'homepages/login.html', context)
        else:
            patient = Patient()

            patient.first_name = request.POST['first_name']
            patient.last_name = request.POST['last_name']
            patient.username = request.POST['username']
            patient.password = request.POST['password']
            patient.age = request.POST['age']
            patient.weight = request.POST['weight']
            patient.height = request.POST['height']
            patient.address1 = request.POST['address1']
            patient.address2 = request.POST['address2']
            patient.city = request.POST['city']
            patient.state = request.POST['state']
            patient.zip = request.POST['zip']
            patient.email = request.POST['email']
            patient.phone = request.POST['phone']

            patient.save()

            loggedIn = True
            loggedInPatientId = patient.id
            loggedInUsername = patient.username
            
            return indexPageView(request)

    elif request.method == 'POST' and method == "loginform":
        
        username = request.POST['username']
        password = request.POST['password']
        notFound = False

        data = Patient.objects.all()

        for patient in data:
            if username == patient.username and password == patient.password:
                loggedIn = True
                loggedInPatientId = patient.id
                loggedInUsername = patient.username
                return indexPageView(request)
            else :
                notFound = True
            
        if notFound:
            context = {
                "display" : "login",
                "errors" : "The username or password are incorrect"
            }
            return render(request, 'homepages/login.html', context)
    else:

        if method == "landing" :
            context = {
                "display" : "original"
            }
        elif method == "create":
            context = {
                "display" : "create"
            }
        else :
            context = {
                "display" : "login",
                "errors" : ""
            }

        return render(request, 'homepages/login.html', context)

def AboutPageView(request):
    data = Patient_Condition.objects.all()
    user_condition = []
    for condtion in data:
        if condtion.patient.username == loggedInUsername:
            user_condition.append(data)
   
    context = {
            "condtions": user_condition
        }

    return render(request, 'homepages/about.html', context)
# def apiPageView(request) :
#     response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={settings.API_KEY}&query=Cheddar%20Cheese').json()
#     print(response)
#     return render(request,'homepages/apitest.html',{'response':response})


def apiJSONView(request) :
    response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query=apple&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=asc&api_key={settings.API_KEY}').json()
    return JsonResponse(response)


def LogFoodPageView(request) :
    food_names = {}
    current_date = dt.now().date()
    formatted_date = f'{current_date.strftime("%b")} {current_date.strftime("%d")}, {current_date.strftime("%Y")}'

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
                    # adding the new things to our list - may be unneccessary...
                    nutrient_table.append(nutrient['nutrientName'])
                    

                # check if the food/nutrient combination has already been recorded in the database
                # if not, load it up and send it over!
                if not f"{searched_food['description']}: {nutrient['nutrientName']}" in nutrient_in_food_table :
                    nutrient_in_food_data = Nutrient_In_Food(
                        nutrient = Nutrient.objects.get(nutrient_name= nutrient['nutrientName']),
                        food = Food.objects.get(food_name= searched_food['description']),
                        measurement = Measurement.objects.get(description= nutrient['unitName']),
                        amount = nutrient['value'],
                    )
                    nutrient_in_food_data.save()
                    # adding the new things to our list - may be unneccessary...
                    nutrient_in_food_table.append(f"{searched_food['description']}: {nutrient['nutrientName']}")

        patient_logs_food_data = Patient_Logs_Food(
            food = Food.objects.get(food_name= searched_food['description']),
            patient = Patient.objects.get(username= loggedInUsername),
            measurement = Measurement.objects.get(description= "Servings"),
            quantity = post_form_data['numServings'],
            date_time = post_form_data['dateTime'],
        )
        patient_logs_food_data.save()

        # thought i would need this data but didn't
        # searched_food_form_data = Food.objects.all()
        # measurement_form_data = Measurement.objects.all()
        # nutrient_form_data = Nutrient.objects.all()
        # nutrient_in_food_form_data = Nutrient_In_Food.objects.all()


        # all_form_data = {
        #     'food' : searched_food_form_data,
        #     'measurement' : measurement_form_data,
        #     'nutrient' : nutrient_form_data,
        #     'nutrient_in_food' : nutrient_in_food_form_data
        # }

    return render (request, 'homepages/logfood.html', { "food_names": 
    food_names, "formatted_date": formatted_date} )


def PickFavoritesPageView(request):

    context = {
        'dummy' : 'data'
    }

    return render(request, 'homepages/pickfavorites.html', context)

