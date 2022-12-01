from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
import json
from homepages.models import Food, Nutrient, Patient, Alert, Nutrient_In_Food

loggedIn = False
loggedInUsername = ""
loggedInPatientId = None

def indexPageView(request):
    global loggedInPatientId
    if loggedInPatientId != None:
        data = Nutrient_In_Food.objects.all()
        patientData = Patient.objects.get(id = loggedInPatientId)

        context = {
            'data':data,
            'patientData' : patientData,
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
        return render(request,'homepages/diary.html')
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




