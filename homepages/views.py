from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
import json
from homepages.models import Food, Nutrient, Patient, Alert, Nutrient_In_Food, Patient_Logs_Food, Measurement
import datetime

loggedIn = False
loggedInUsername = ""
loggedInPatientId = None

def indexPageView(request):
    global loggedInPatientId
    if loggedInPatientId != None:
        data = Nutrient_In_Food.objects.all()
        patientData = Patient.objects.get(id = loggedInPatientId)
        nutrientNames = Nutrient.objects.all()
        current_date = datetime.datetime.now().date()
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

                if food.date_time.date() == datetime.today().date():
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
    return render(request, 'homepages/about.html')

# this is so I can see what is being returned to visualize how to deal with it in the below code
def apiJSONView(request) :
    response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query=banana&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=asc&api_key={settings.API_KEY}').json()
    return JsonResponse(response)


def LogFoodPageView(request) :
    food_names = {}

    if 'name' in request.GET:
        name = request.GET['name']
        response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={name}&dataType=&pageSize=8&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
        data = response.json()
        searchedFoods = data['foods']
 
        for idx, food in enumerate(searchedFoods) :
            food_names['food_name' + str(idx+1)] = food['description']
    

    if request.method == "POST":
        post_form_data = request.POST
        print(post_form_data['food_names_options'])
        print(post_form_data['numServings'])
        print(post_form_data['dateTime'])

        all_form_data = {}
        searched_food = {}
        searched_food_data = {}
        food_nutrients = {}
        food_found = False

        nutrientList = [
            'Protein',
            'Potassium, K',
            'Carbohydrate, by difference',
            'Sodium, Na',
            'Water',
            'Phosphorus, P',
        ]

        # get the name of the food they typed in and send it call the api with it!
        name = f"{post_form_data['food_names_options']}"
        response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={name}&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
        # turn it into json to be able to deal with the info we get
        data = response.json()
        # keep just the info about the specific FOOD and from only the FIRST one returned
        searched_food = data['foods'][0]

        # the database food table accessible to us in a for loop
        food_table = Food.objects.all()
        
        # the database nutrient table accessible to us in list (if/in)
        nutrient_table = []
        for a_nutrient in Nutrient.objects.all() :
            # print(a_nutrient)
            nutrient_table.append(f'{a_nutrient}')

        # the database nutrient_in_food table accessible to us in list (if/in)
        nutrient_in_food_table = []
        for a_nutrient_in_food in Nutrient_In_Food.objects.all() :
            # print(a_nutrient_in_food)
            nutrient_in_food_table.append(f'{a_nutrient_in_food}')

        # the database measurement table accessible to us in list (if/in)
        measurement_table = []
        for a_measurement in Measurement.objects.all() :
            # print(a_measurement)
            measurement_table.append(f'{a_measurement}')


        # checking the database for the inputed food
        food_found = False
        for a_food in food_table :
            if searched_food['description'] == a_food.food_name :
                food_found = True

        # load it up to be ready to save in the database if it's not found!
        if not food_found: 
            food_data = Food(
                food_name = searched_food['description']
            )
            # send it over to the database!
            food_data.save()
            

        # get all the nutrients from the searched foods and check if it's 
        # nutrients that we care about
        for nutrient in searched_food['foodNutrients'] :
            if nutrient['nutrientName'] in nutrientList:
                food_nutrients[ nutrient['nutrientName'] ] = [{ 'value' : nutrient['value']}, {'unitName' : nutrient['unitName']}]
                # if they are not already in the database, load it up and send it over!

                if not nutrient['unitName'] in measurement_table:
                    measurement_data = Measurement(
                        description = nutrient['unitName'],
                    )
                    measurement_data.save()
                    # adding the new things to our list - may be unneccessary...
                    measurement_table.append(nutrient['unitName'])

                if not nutrient['nutrientName'] in nutrient_table:
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
    food_names} )


def PickFavoritesPageView(request):

    context = {
        'dummy' : 'data'
    }

    return render(request, 'homepages/pickfavorites.html', context)

