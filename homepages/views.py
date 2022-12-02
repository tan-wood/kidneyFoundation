from django.shortcuts import render
from django.http import JsonResponse
import requests
from django.conf import settings
import json
from homepages.models import Food, Nutrient, Patient, Alert, Nutrient_In_Food, Patient_Logs_Food, Measurement, Patient_Condition, Condition, Patient_Favorite_Food, Alert_Type
from datetime import datetime as dt
import random
import time

loggedIn = False
loggedInUsername = ""
loggedInPatientId = None

nutrientList = [
    'Protein',
    'Potassium, K',
    'Carbohydrate, by difference',
    'Sodium, Na',
    'Water',
    'Phosphorus, P',
    'Sugars, total including NLEA',
]

def indexPageView(request):
    global loggedInPatientId
    global loggedInUsername

    """
    # Recommended Daily Amounts:
    Protein                         0.6 g / kg
    Potassium, K                    3000 mg
    Carbohydrate, by difference     250 g
    Sodium, Na                      2300 mg
    Water                           1800 g
    Phosphorus, P                   3500 mg
    Sugar                           30 g
    """

    if loggedInPatientId != None:

        patientData = Patient.objects.get(id = loggedInPatientId)
        nutrientData = Nutrient.objects.all()
        
        # Filter Nutrient Data down to the logged in users nutrients from today
        allNutrientInFoodData = Nutrient_In_Food.objects.all()


        loggedFoods = Patient_Logs_Food.objects.all()
        nutrients = []

        currentProteinAmount = 0
        currentPotassiumAmount = 0
        currentCarbAmount = 0
        currentSodiumAmount = 0
        currentWaterAmount = 0
        currentPhosphorusAmount = 0
        currentSugarAmount = 0

        for food in loggedFoods:
            if food.patient.username == loggedInUsername and food.date_time.date() == dt.today().date():
                # The foods here will be from the right user and will be today
                num_servings = food.quantity
                for nutrient in allNutrientInFoodData:
                    if nutrient.food.food_name == food.food.food_name:
                        if nutrient.nutrient.nutrient_name == "Protein":
                            currentProteinAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Potassium, K":
                            currentPotassiumAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Carbohydrate, by difference":
                            currentCarbAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Sodium, Na":
                            currentSodiumAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Water":
                            currentWaterAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Phosphorus, P":
                            currentPhosphorusAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Sugars, total including NLEA":
                            currentSugarAmount += round(nutrient.amount * num_servings, 2)

        # Recommended Amounts
        patientKG = patientData.weight * 0.453592
        proteinAmount = patientKG * 0.6
        


        for nutrient in nutrientData:
            currentAmount = 0
            recommendedAmount = 0
            recMeasurement = ''
            if nutrient.nutrient_name == "Protein":
                currentAmount = round(currentProteinAmount, 2)
                recommendedAmount = round(proteinAmount, 0)
                recMeasurement = "G"
            elif nutrient.nutrient_name == "Potassium, K":
                currentAmount = round(currentPotassiumAmount, 2)
                recommendedAmount = 3000
                recMeasurement = "MG"
            elif nutrient.nutrient_name == "Carbohydrate, by difference":
                currentAmount = round(currentCarbAmount, 2)
                recommendedAmount = 250
                recMeasurement = "G"
            elif nutrient.nutrient_name == "Sodium, Na":
                currentAmount = round(currentSodiumAmount, 2)
                recommendedAmount = 2300
                recMeasurement = "MG"
            elif nutrient.nutrient_name == "Water":
                currentAmount = round(currentWaterAmount, 2)
                recommendedAmount = 1800
                recMeasurement = "G"
            elif nutrient.nutrient_name == "Calcium":
                currentAmount = round(currentWaterAmount, 2)
                recommendedAmount = 1800
                recMeasurement = "G"
            elif nutrient.nutrient_name == "Phosphorus, P":
                currentAmount = round(currentPhosphorusAmount, 2)
                recommendedAmount = 1500
                recMeasurement = "MG"
            elif nutrient.nutrient_name == "Sugars, total including NLEA":
                currentAmount = round(currentSugarAmount, 2)
                recommendedAmount = 30
                recMeasurement = "G"
            # Each nutrient needs a new object
            nutrient_object = {
                'nutrient' : nutrient,
                'currentAmount' : currentAmount,
                'dailyAmount' : recommendedAmount,
                'measurement' : recMeasurement
            }
            nutrients.append(nutrient_object)




        # Food Suggestions
        # Step 1: Find the two nutrients that are closest to going over
        #         the recommended amount
        nutriMax = 0
        nutriMaxName = ""
        nutri2Max = 0
        nutri2MaxName = ""
        favNutriMin = 99999
        favNutriMinName = ""
        favNutri2Min = 99999
        favNutri2MinName = ""
        favFoodNutriMin = ""
        favFoodNutri2Min = ""
        favoriteFoods = ""

        randomSeed1 = 0
        randomSeed2 = 0

        random_food_list = []


        max_nutrients_in_foods = {}
        
        for a_nutrient in nutrients :
            print('-----')
            print(a_nutrient['nutrient'])
            print(a_nutrient['currentAmount'])
            print(a_nutrient['dailyAmount'])
            nutrient_level = a_nutrient['currentAmount'] / a_nutrient['dailyAmount']

            if nutrient_level > nutriMax:
                nutri2Max = nutriMax
                nutri2MaxName = nutriMaxName
                nutriMax = nutrient_level
                nutriMaxName = a_nutrient
            elif nutriMax > nutrient_level > nutri2Max:
                nutri2Max = nutrient_level
                nutri2MaxName = a_nutrient



        if nutriMax == 0 and nutri2Max == 0 :
            favoriteFoods = Patient_Favorite_Food.objects.all()
            for favoriteFood in favoriteFoods :
                if favoriteFood.patient.id == loggedInPatientId :
                    random_food_list.append(favoriteFood.food.food_name)
        
            if len(random_food_list) > 2 :
                randomSeed1 = random.randint(0, (len(random_food_list)-1))
                randomSeed2 = random.randint(0, (len(random_food_list)-2))

                favFoodNutriMin = random_food_list[randomSeed1]
                random_food_list.pop(randomSeed1)
                favFoodNutri2Min = random_food_list[randomSeed2]


            suggested_foods = {
                "suggestion1" : favFoodNutriMin,
                "nutrient_for_suggestion1" : "",
                "nutrient_amount_in_suggestion1" : "",
                "suggestion2" : favFoodNutri2Min,
                "nutrient_for_suggestion2" : "",
                "nutrient_amount_in_suggestion2" : "",
                "desc" : "From your favorites"
            }



        else :

            # Print them out to see if it worked
            # print(nutriMaxName['nutrient'])
            # print (round((nutriMax),4))
            # print(nutri2MaxName['nutrient'])
            # print (round((nutri2Max),4))

            # Step 2: Find which favorite food has the lowest in max nutrient 1
            #         Find which favorite food has the lowest in max nutrient 2
            favoriteFoods = Patient_Favorite_Food.objects.all()
            # print(favoriteFoods)
            for favoriteFood in favoriteFoods :
                # print("\n----\nFavorite Food: " + str(favoriteFood.patient.first_name))
                # print(favoriteFood.patient.id, loggedInPatientId)
                if favoriteFood.patient.id == loggedInPatientId :
                    for nutrient in allNutrientInFoodData:
                        # print("Nutrient: " + str(nutrient))
                        # print(nutrient.food.food_name, nutrient.nutrient.nutrient_name, favoriteFood.food.food_name)
                        if nutrient.food.food_name == favoriteFood.food.food_name:
                            # print("HELLO")
                            # print(nutrient.food.food_name, favoriteFood.food.food_name)
                            if nutrient.nutrient.nutrient_name == str(nutriMaxName['nutrient']) :
                                if nutrient.amount < favNutriMin :
                                    favFoodNutriMin = nutrient.food.food_name
                                    favNutriMin = nutrient.amount
                                    favNutriMinName = nutrient.nutrient.nutrient_name
                            if nutrient.nutrient.nutrient_name == str(nutri2MaxName['nutrient']) :
                                if nutrient.amount < favNutri2Min :
                                    favFoodNutri2Min = nutrient.food.food_name
                                    favNutri2Min = nutrient.amount
                                    favNutri2MinName = nutrient.nutrient.nutrient_name
            # print(" ")
            # print(" ")
            # print(" ")
            # print("LoggedIn Username: " + str(loggedInUsername))
            # print(" ")
            # print(" ")
            # print(" ")
            # print(favFoodNutriMin)
            # print(favNutriMinName)
            # print(favNutriMin)
            # print(favFoodNutri2Min)
            # print(favNutri2MinName)
            # print(favNutri2Min)


            suggested_foods = {
                "suggestion1" : favFoodNutriMin,
                "nutrient_for_suggestion1" : favNutriMinName,
                "nutrient_amount_in_suggestion1" : favNutriMin,
                "suggestion2" : favFoodNutri2Min,
                "nutrient_for_suggestion2" : favNutri2MinName,
                "nutrient_amount_in_suggestion2" : favNutri2Min,
                "desc" : "Low in "
            }


        context = {
            'data' : allNutrientInFoodData,
            'patientData' : patientData,
            'nutrients' : nutrients,
            'suggested_foods' : suggested_foods,
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
                a = Alert.objects.get(id=alert.id)
                a.unread = False  # change field
                a.save() # this will update only
        
        context = {
            "alerts": user_alerts,
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
            "past_foods" : user_past_foods,
        }

        return render(request,'homepages/diary.html', context)
    else:
        return LandingPageView(request)

def AccountPageView(request, method):
    
    if loggedInPatientId != None:
        if request.method == 'POST' and method == "editPatientForm":
            patient_id = loggedInPatientId

            patient = Patient.objects.get(id = patient_id)

            patient.first_name = request.POST['first_name']
            patient.last_name = request.POST['last_name']
            patient.age = request.POST['age']
            patient.weight = request.POST['weight']
            patient.height = (int(float(request.POST['height_ft']))*12) + (int(float(request.POST['height_in'])))
            patient.email = request.POST['email']
            patient.phone = request.POST['phone']

            patient.save()

            condition_list = ['High Blood Pressure', 'Diabetes']

            for i in range(len(condition_list)):
                if request.POST[condition_list[i]] == "Yes":
                    condition = Condition.objects.get(description=condition_list[i])
                    try:
                        patient_condition = Patient_Condition.objects.get(patient_id=loggedInPatientId, condition_id=condition.id)
                        pass
                    except:
                        Patient_Condition.objects.create(patient_id=loggedInPatientId, condition_id=condition.id)
                else:
                    condition = Condition.objects.get(description=condition_list[i])
                    try:
                        patient_condition = Patient_Condition.objects.get(patient_id=loggedInPatientId, condition_id=condition.id)
                        patient_condition.delete()
                    except:
                        pass


            return AccountPageView(request, "homeAccount")
        elif request.method == 'POST' and method == "changeUandPForm":
            patient_id = loggedInPatientId

            patient = Patient.objects.get(id = patient_id)

            patient.username = request.POST['username']
            patient.password = request.POST['password']

            patient.save()

            return AccountPageView(request, "homeAccount")
        else:     
            patientData = Patient.objects.get(id = loggedInPatientId)
            patientConditions = Patient_Condition.objects.all()
            loggedInPatientConditions = []

            for patient in patientConditions:
                if patient.patient_id == loggedInPatientId:
                    loggedInPatientConditions.append(Condition.objects.get(id = patient.condition_id))

            condition_data = Condition.objects.all()

            inches = patientData.height % 12
            feet = (patientData.height - inches)/12

            if method == "homeAccount":
                context = {
                    'patientData' : patientData,
                    'display': "homeAccount",
                    'conditions' : loggedInPatientConditions,
                    'condition_data' : condition_data,
                    'inches': inches,
                    'feet': feet
                }
            elif method == "editPatient":
                context = {
                    'patientData' : patientData,
                    'display': "editPatient",
                    'conditions' : loggedInPatientConditions,
                    'condition_data' : condition_data,
                    'inches': inches,
                    'feet': feet
                }
            else:
                context = {
                    'patientData' : patientData,
                    'display': "changeLoginInfo",
                    'conditions' : loggedInPatientConditions,
                    'condition_data' : condition_data,
                }
    if loggedIn:
        return render(request,'homepages/account.html', context)
    else:
        return LandingPageView(request)

def LandingPageView(request):
    global loggedIn

    servings_found = False
    measurement_datacheck = Measurement.objects.all()
    for a_measurement in measurement_datacheck :
        if a_measurement.description == "Servings":
            servings_found = True
            continue

    if not servings_found :
        preset_measurement_data = Measurement(
            description = "Servings"
        )
        preset_measurement_data.save()

    condition1_found = False
    condition2_found = False

    condition_datacheck = Condition.objects.all()
    for a_condition in condition_datacheck :
        if a_condition.description == "High Blood Pressure":
            condition1_found = True
        if a_condition.description == "Diabetes":
            condition2_found = True

    if not condition1_found :
        preset_condition1_data = Condition(
            description = "High Blood Pressure"
        )
        preset_condition1_data.save()

    if not condition2_found :
        preset_condition2_data = Condition(
            description = "Diabetes"
        )
        preset_condition2_data.save()

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
    errors = []
    errors.clear()
    if request.method == 'POST' and method == "form":
        email = request.POST['email']
        username = request.POST['username']

        data = Patient.objects.all()

        for patient in data:
            if email == patient.email:
                errors.append("This email has already been registered") 
            if username == patient.username:
                errors.append("This username is already taken")
        
        condition_data = Condition.objects.all()

        if len(errors) != 0:
            context = {
                    "display" : "create",
                    "errors" : errors,
                    "condition_data": condition_data,
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
            patient.height = (int(float(request.POST['height_ft']))*12) + (int(float(request.POST['height_in'])))
            patient.email = request.POST['email']
            patient.phone = request.POST['phone']

            patient.save()

            if request.POST['High Blood Pressure'] == "Yes":

                condition = Condition.objects.get(description="High Blood Pressure")
                patientId = Patient.objects.get(id=patient.id)
                Patient_Condition.objects.create(patient_id=patientId.id, condition_id=condition.id)
                
                
            
            if request.POST['Diabetes'] == "Yes":

                condition = Condition.objects.get(description="Diabetes")
                patientId = Patient.objects.get(id=patient.id)
                Patient_Condition.objects.create(patient_id=patientId.id, condition_id=condition.id)

            

            loggedIn = True
            loggedInPatientId = patient.id
            loggedInUsername = patient.username
            
            return PickFavoritesPageView(request)

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
                "errors" : "The username or password is incorrect"
            }
            return render(request, 'homepages/login.html', context)
    else:

        if (method == "landing" or method == "create" or method == "login") and loggedIn:
            return indexPageView(request)
        elif method == "landing" :
            context = {
                "display" : "original"
            }
        elif method == "create":

            condition_data = Condition.objects.all()

            context = {
                "display" : "create",
                "condition_data": condition_data,
            }
        else :
            context = {
                "display" : "login",
                "errors" : ""
            }

        return render(request, 'homepages/login.html', context)

def AboutPageView(request):
    global loggedIn
    patientConditions = Patient_Condition.objects.all()
    loggedInPatientConditions = []

    for patient in patientConditions:
        if patient.patient_id == loggedInPatientId:
            condition_obj = Condition.objects.get(id = patient.condition_id)
            loggedInPatientConditions.append(condition_obj.description)

    if not loggedIn:
        context = {
            "signedIn": False
        }
    else:
        context = {
            "signedIn": True,
            "conditions": loggedInPatientConditions,
        }

    return render(request, 'homepages/about.html', context)
# def apiPageView(request) :
#     response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?api_key={settings.API_KEY}&query=Cheddar%20Cheese').json()
#     print(response)
#     return render(request,'homepages/apitest.html',{'response':response})


def apiJSONView(request) :
    response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query=burger&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=asc&api_key={settings.API_KEY}').json()
    return JsonResponse(response)


def LogFoodPageView(request) :

    food_names = {}
    current_date = dt.now().date()
    formatted_date = f'{current_date.strftime("%b")} {current_date.strftime("%d")}, {current_date.strftime("%Y")}'
    display_chart = False
    food_nutrients = {}
    food_nutrients2 = []
    searched_food_title = ""

    nutrientList = [
    'Protein',
    'Potassium, K',
    'Carbohydrate, by difference',
    'Sodium, Na',
    'Water',
    'Phosphorus, P',
    ]

    if 'name' in request.GET:
        name = request.GET['name']
        response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={name}&dataType=&pageSize=8&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
        data = response.json()
        searchedFoods = data['foods']

        for idx, food in enumerate(searchedFoods) :
            food_names['food_name' + str(idx+1)] = food['description']
    

    if request.method == "POST":
        display_chart = True
        post_form_data = request.POST
        # print(post_form_data['food_names_options'])
        # print(post_form_data['numServings'])
        # print(post_form_data['dateTime'])

        all_form_data = {}
        searched_food = {}
        searched_food_data = {}
        food_found = False

        global nutrient_list

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
                food_name = searched_food['description'],
            )
            # send it over to the database!
            food_data.save()
            

        # get all the nutrients from the searched foods and check if it's 
        # nutrients that we care about
        searched_food_title = searched_food['description']
        for nutrient in searched_food['foodNutrients'] :
            if nutrient['nutrientName'] in nutrientList:
                food_nutrients[ nutrient['nutrientName'] ] = [{ 'value' : nutrient['value']}, {'unitName' : nutrient['unitName']}]
                nutrient_object = {
                    'name' : nutrient['nutrientName'],
                    'value' : nutrient['value'],
                    'unitName' : nutrient['unitName']
                }
                food_nutrients2.append(nutrient_object)
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


        # Create alerts
        allNutrientInFoodData = Nutrient_In_Food.objects.all()
        loggedFoods = Patient_Logs_Food.objects.all()
        patientData = Patient.objects.get(id = loggedInPatientId)

        currentProteinAmount = 0
        currentPotassiumAmount = 0
        currentCarbAmount = 0
        currentSodiumAmount = 0
        currentWaterAmount = 0
        currentPhosphorusAmount = 0
        currentSugarAmount = 0

        for food in loggedFoods:
            if food.patient.username == loggedInUsername and food.date_time.date() == dt.today().date():
                num_servings = food.quantity
                for nutrient in allNutrientInFoodData:
                    if nutrient.food.food_name == food.food.food_name:
                        if nutrient.nutrient.nutrient_name == "Protein":
                            currentProteinAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Potassium, K":
                            currentPotassiumAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Carbohydrate, by difference":
                            currentCarbAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Sodium, Na":
                            currentSodiumAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Water":
                            currentWaterAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Phosphorus, P":
                            currentPhosphorusAmount += round(nutrient.amount * num_servings, 2)
                        elif nutrient.nutrient.nutrient_name == "Sugars, total including NLEA":
                            currentSugarAmount += round(nutrient.amount * num_servings, 2)

        patientKG = patientData.weight * 0.453592
        proteinAmount = patientKG * 0.6

        """
        # Recommended Daily Amounts:
        Protein                         0.6 g / kg
        Potassium, K                    3000 mg
        Carbohydrate, by difference     250 g
        Sodium, Na                      2300 mg
        Water                           3700 mg
        Phosphorus, P                   3500 mg
        Sugar                           30 g
        """

        if currentProteinAmount > proteinAmount:
            alert_name = "High Protein Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your protein levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentPotassiumAmount > 3000:
            alert_name = "High Potassium Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your potassium levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentCarbAmount > 250:
            alert_name = "High Carb Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your carbohydrate levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentSodiumAmount > 2300:
            alert_name = "High Sodium Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your sodium levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentWaterAmount > 3700:
            alert_name = "High Water Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your water levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentPhosphorusAmount > 3500:
            alert_name = "High Phosphorus Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your phosphorus levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

        if currentSugarAmount > 30:
            alert_name = "High Sugar Levels"
            allAlertTypes = Alert_Type.objects.all()
            alert_type_names = []
            for alert_type in allAlertTypes:
                alert_type_names.append(alert_type.name)
            if alert_name not in alert_type_names:
                alert_type_object = Alert_Type(
                    name = alert_name,
                    description = "Your sugar levels exceed the recommended amount"
                )
                alert_type_object.save()

            alert_object = Alert(
                date_time = dt.now(),
                unread = True,
                alert_type = Alert_Type.objects.get(name = alert_name),
                patient = Patient.objects.get(id = loggedInPatientId)
            )
            alert_object.save()

    print(food_nutrients)
    print("-----")
    print()


    return render (request, 'homepages/logfood.html', { "food_names": 
    food_names, "display_chart": display_chart, "food_nutrients": food_nutrients, "food_nutrients2": food_nutrients2,
    'searched_food_title' : searched_food_title} )




    # if request.method == "GET":
    #     food_nutrients2 = {}
    #     searched_food2 = {}

    #     foodName = request.GET.get('passedFood')
    #     response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={foodName}&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
    #     # turn it into json to be able to deal with the info we get
    #     data = response.json()
    #     # keep just the info about the specific FOOD and from only the FIRST one returned
    #     searched_food2 = data['foods'][0]

    #     for nutrient in searched_food2['foodNutrients'] :
    #         if nutrient['nutrientName'] in nutrientList:
    #             food_nutrients2[ nutrient['nutrientName'] ] = [{ 'value' : nutrient['value']}, {'unitName' : nutrient['unitName']}]
        
    #     context = {
    #         "nutrient_info": food_nutrients2,
    #         "formatted_date" : formatted_date
    #     }

    #     return render (request, 'homepages/logfood.html', context)

def PickFavoritesPageView(request):

    save = False
    
    food_dict = {
        'Muffin, wheat bran' : 'branMuffin.jpg', #1,1 done
        'Oatmeal, multigrain': 'oatmeal.jpg', #1,2 done
        'Fish, cod, baked or broiled' : 'bakedCod.jpg', #1,3 done
        'Pear, raw': 'pear.jpg',   #1,4 done 
        'Caesar salad, with romaine, no dressing' : 'chickenCaeser.jpg', #1,5 done
        'Eggplant parmesan casserole, regular' : 'eggplant.jpg', #1,6 done
        'Macaroni or pasta salad with shrimp' : 'shrimpPasta.jpg', #1,7 done
        'Raspberries, raw' : 'raspberries.jpg',#1,8 done
        'Fish, salmon, grilled': 'grilledSalmon.jpg', #1,9 done
        'Mixed salad greens, raw': 'mixedGreens.jpg', #1, 10 done
        'Peach, raw' : 'peach.jpg', #1, 11 done
        'Bread, whole wheat, toasted': 'wheatToast.jpg', #1, 12 done
        'Chicken fillet, grilled' : 'grilledChicken.jpg', #1, 13
        'Turkey or chicken burger, on wheat bun' : 'turkeyBurger.jpg', #1, 14 done
        'Fruit smoothie, light' : 'smoothie.jpg', #1, 15 done
        'Orange, raw' : 'orange.jpg' #1,16
    }
    

    global nutrient_list
    food_nutrients = {}
    clicked_food = {}

    if request.method == 'POST':
        favfoods = request.POST.getlist('foods')
        print(favfoods)

        for favfood in favfoods :
            print(favfood)
            response=requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={favfood}&dataType=&pageSize=1&pageNumber=1&sortBy=dataType.keyword&sortOrder=desc&api_key={settings.API_KEY}')
            # turn it into json to be able to deal with the info we get
            data = response.json()
            # keep just the info about the specific FOOD and from only the FIRST one returned

            clicked_food = data['foods'][0]


            food_table = Food.objects.all()

            # checking the database for the inputed food
            food_found = False
            for a_food in food_table :
                if clicked_food['description'] == a_food.food_name :
                    food_found = True

            # load it up to be ready to save in the database if it's not found!
            if not food_found: 
                food_data = Food(
                    food_name = clicked_food['description'],
                )
                # send it over to the database!
                food_data.save()


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


                # get all the nutrients from the searched foods and check if it's 
            # nutrients that we care about
            for nutrient in clicked_food['foodNutrients'] :
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
                    if not f"{clicked_food['description']}: {nutrient['nutrientName']}" in nutrient_in_food_table :
                        nutrient_in_food_data = Nutrient_In_Food(
                            nutrient = Nutrient.objects.get(nutrient_name= nutrient['nutrientName']),
                            food = Food.objects.get(food_name= clicked_food['description']),
                            measurement = Measurement.objects.get(description= nutrient['unitName']),
                            amount = nutrient['value'],
                        )
                        nutrient_in_food_data.save()
                        # adding the new things to our list - may be unneccessary...
                        nutrient_in_food_table.append(f"{clicked_food['description']}: {nutrient['nutrientName']}")
                # THIS IS FOR MAKING PATIENT FAVORITE FOOD NOT DUPLICATABLE
                #  BUT IT DO NOT BE WORKING I need to figure out how to access the current user and put the firstname into a string to check if it's already there
                # patient_favorite_food_table = Patient.objects.all()
                # for a_patient_favorite_food in patient_favorite_food_table :
                #     if a_patient_favorite_food.patient.id == loggedInPatientId :
                #         print(f'{a_patient_favorite_food.patient.first_name}: {a_patient_favorite_food}')
                #         patient_favorite_food_table.append(f'{a_patient_favorite_food}')

            patient_favorite_food_data = Patient_Favorite_Food(
                patient = Patient.objects.get(username= loggedInUsername),
                food = Food.objects.get(food_name= clicked_food['description']),
                is_favorite = True
            )

            patient_favorite_food_data.save()

            save = True

        

     
    context = {
        'food_dict' : food_dict
    }

    
    if save :
        time.sleep(5)
        return indexPageView(request)
    else:
        return render(request, 'homepages/pickfavorites.html', context)


def DiaryItemPageView(request, item_id):

    # Get the patientLogsFood item where id is item_id
    patientFoodData = Patient_Logs_Food.objects.get(id = item_id)

    # Get the nutrients in the food
    nutrientInFoodData = Nutrient_In_Food.objects.all()
    nutrientInFoodList = []
    nutrientInFoodNames = []
    for nutrientInFood in nutrientInFoodData:
        if nutrientInFood.food.food_name == patientFoodData.food.food_name and nutrientInFood.nutrient.nutrient_name not in nutrientInFoodNames:
            nutrient_object = {
                'name': nutrientInFood.nutrient.nutrient_name,
                'value': nutrientInFood.amount,
                'unitName': nutrientInFood.measurement
            }
            nutrientInFoodList.append(nutrient_object)
            nutrientInFoodNames.append(nutrientInFood.nutrient.nutrient_name)


    context = {
        'item' : patientFoodData,
        'nutrientInFoodList' : nutrientInFoodList
    }

    return render(request, 'homepages/diary_item.html', context)

def DeleteItemPageView(request, item_id):

    if loggedIn:

        patientFoodData = Patient_Logs_Food.objects.filter(id = item_id).delete()

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
            "past_foods" : user_past_foods,
        }

        return render(request,'homepages/diary.html', context)
    else:
        return LandingPageView(request)



def getUsername():
    global loggedInUsername
    return loggedInUsername
